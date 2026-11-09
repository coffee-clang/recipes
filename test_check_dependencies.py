#!/usr/bin/env python3
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
from check_dependencies import (
    HOST_TOOLS,
    AliasCollision,
    _check_dependencies,
    check_dependencies,
    collect_recipes,
    main,
    resolve,
)
from recipe_metadata import (
    RECIPES_DIR,
    load_recipe,
    parse_dependencies,
    recipe_files,
)

REPO_ROOT = Path(__file__).resolve().parent


def make_recipe(root, name, canonical_name, deps, output_type="library",
                build_deps=None):
    """Write a minimal recipe whose directory name is `name`."""
    d = root / name[0] / name
    d.mkdir(parents=True)
    lines = [
        f'title = "{name}"',
        'version = "1.0.0"',
        'description = "Test."',
        'license = "MIT"',
        f'canonical_name = "{canonical_name}"',
        'recipe_url = "https://example.com/x.git"',
        f'output_type = "{output_type}"',
    ]
    if deps is not None:
        lines.append("[dependencies]")
        for dep in deps:
            lines.append(f'{dep} = ""')
    if build_deps is not None:
        lines.append("[build-dependencies]")
        lines += [f'{tool} = ""' for tool in build_deps]
    (d / "library.toml").write_text("\n".join(lines) + "\n")
    (d / "install.sh").write_text("#!/bin/bash\n")
    return d


class TestCollectRecipes(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_collects_canonical_name_and_dependencies(self):
        make_recipe(self.root, "zlib", "zlib", [])
        make_recipe(self.root, "curl", "curl", ["zlib", "openssl"])

        recipes = collect_recipes(self.root)
        self.assertEqual(set(recipes), {"zlib", "curl"})
        self.assertEqual(set(recipes["curl"]["deps"]), {"zlib", "openssl"})

    def test_directory_name_is_registered_as_an_alias(self):
        make_recipe(self.root, "jpegdir", "libjpeg_turbo", [])
        self.assertEqual(set(collect_recipes(self.root)),
                         {"libjpeg_turbo", "jpegdir"})

    def test_returns_empty_for_missing_root(self):
        self.assertEqual(collect_recipes(self.root / "nope"), {})


class TestAliasCollision(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_collision_raises_with_both_paths(self):
        # One recipe's directory name shadowing another's canonical name.
        make_recipe(self.root, "shared", "libfoo", [])
        make_recipe(self.root, "other", "shared", [])

        with self.assertRaises(AliasCollision) as ctx:
            collect_recipes(self.root)
        self.assertEqual(ctx.exception.name, "shared")
        self.assertIn("shared", str(ctx.exception))
        self.assertNotEqual(ctx.exception.first, ctx.exception.second)

    def test_one_recipe_under_two_names_is_not_a_collision(self):
        make_recipe(self.root, "jpegdir", "libjpeg_turbo", [])
        recipes = collect_recipes(self.root)
        self.assertEqual(recipes["libjpeg_turbo"]["path"],
                         recipes["jpegdir"]["path"])

    def test_helper_raises_alias_collision(self):
        # The private helper must raise, not report, a structural failure.
        # It is the unit under test (not main) because raise-vs-report is its
        # contract: main catches the exception and turns it into an error
        # line, so asserting through the CLI would test main's reporting, not
        # the helper's refusal to continue on a broken tree.
        make_recipe(self.root, "shared", "libfoo", [])
        make_recipe(self.root, "other", "shared", [])
        with self.assertRaises(AliasCollision):
            _check_dependencies(self.root)


class TestCheckDependencies(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_no_recipes_is_an_error_not_a_pass(self):
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("refusing to report success", errors[0])

    def test_resolved_dependency_passes(self):
        make_recipe(self.root, "zlib", "zlib", [])
        make_recipe(self.root, "curl", "curl", ["zlib"])
        self.assertEqual(check_dependencies(self.root), [])

    def test_unresolved_dependency_fails(self):
        make_recipe(self.root, "curl", "curl", ["zlib"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("curl", errors[0])
        self.assertIn("zlib", errors[0])

    def test_host_tool_in_dependencies_fails(self):
        # [dependencies] lists registry libraries. A tool there is something
        # coffee would try to fetch, and there is no cmake recipe to fetch.
        make_recipe(self.root, "zeromq", "zeromq", ["cmake"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("cmake", errors[0])
        self.assertIn("[build-dependencies]", errors[0])

    def test_host_tool_in_build_dependencies_passes(self):
        self.assertIn("cmake", HOST_TOOLS)
        make_recipe(self.root, "zeromq", "zeromq", [], build_deps=["cmake"])
        self.assertEqual(check_dependencies(self.root), [])

    def test_unknown_build_tool_fails(self):
        make_recipe(self.root, "zeromq", "zeromq", [], build_deps=["nosuchtool"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("nosuchtool", errors[0])

    def test_library_in_build_dependencies_fails(self):
        # A registry library is linked against, so it belongs in
        # [dependencies], where coffee fetches it.
        make_recipe(self.root, "zlib", "zlib", [])
        make_recipe(self.root, "curl", "curl", [], build_deps=["zlib"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("zlib", errors[0])

    def test_unknown_host_tool_fails(self):
        make_recipe(self.root, "zeromq", "zeromq", ["nosuchtool"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("nosuchtool", errors[0])

    def test_empty_dependency_table_declares_nothing(self):
        # This is what recipes/x/xorgproto/library.toml used to spell as the
        # string dependencies = "None", which parsed as three fake packages.
        make_recipe(self.root, "xorgproto", "xorgproto", [])
        self.assertEqual(check_dependencies(self.root), [])

    def test_resolves_by_canonical_name_when_directory_differs(self):
        make_recipe(self.root, "jpegdir", "libjpeg_turbo", [])
        make_recipe(self.root, "tiff", "tiff", ["libjpeg_turbo"])
        self.assertEqual(check_dependencies(self.root), [])

    def test_resolves_by_directory_name_when_it_differs(self):
        make_recipe(self.root, "jpegdir", "libjpeg_turbo", [])
        make_recipe(self.root, "tiff", "tiff", ["jpegdir"])
        self.assertEqual(check_dependencies(self.root), [])

    def test_recipe_referencing_itself_fails(self):
        make_recipe(self.root, "zlib", "zlib", ["zlib"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("itself", errors[0])

    def test_self_reference_by_directory_alias_fails(self):
        make_recipe(self.root, "jpegdir", "libjpeg_turbo", ["jpegdir"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("itself", errors[0])

    def test_reports_all_offenders_not_just_first(self):
        make_recipe(self.root, "alib", "a_lib", ["nope1", "nope2"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 2)

    def test_dashed_directory_name_resolves(self):
        # Eight recipes keep their upstream dashed spelling in the directory
        # name (recipes/l/libjpeg-turbo/ has canonical_name libjpeg_turbo), so
        # the directory spelling is the name dependents use.
        make_recipe(self.root, "libjpeg-turbo", "libjpeg_turbo", [])
        make_recipe(self.root, "tiff", "tiff", ["libjpeg-turbo"])
        self.assertEqual(check_dependencies(self.root), [])

    def test_dashed_spelling_of_an_underscored_only_recipe_fails(self):
        # Resolution is by exact name, not by string munging. A dependency
        # whose dashed form matches nothing is an error to fix in the recipe,
        # not something to paper over.
        make_recipe(self.root, "jpegdir", "libjpeg_turbo", [])
        make_recipe(self.root, "tiff", "tiff", ["libjpeg-turbo"])
        errors = check_dependencies(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("libjpeg-turbo", errors[0])

    def test_every_dashed_dependency_in_the_real_tree_resolves(self):
        # The reason the exact-name rule is safe: the only dashed dependency
        # spellings in the tree are directory names or host tools.
        for toml_file in recipe_files(RECIPES_DIR):
            data = load_recipe(toml_file)
            for dep in parse_dependencies(data.get("dependencies")):
                if "-" not in dep:
                    continue
                with self.subTest(dep=dep, recipe=toml_file.parent.name):
                    self.assertTrue(
                        resolve(dep, collect_recipes(RECIPES_DIR)),
                        f"{dep} does not resolve by exact name",
                    )


class TestSingleParsePass(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        for name in ("zlib", "curl"):
            make_recipe(self.root, name, name, [])

    def test_check_uses_single_parse_pass(self):
        import check_dependencies as checker

        original = checker.load_recipe
        calls = []

        def counting(path):
            calls.append(Path(path))
            return original(path)

        checker.load_recipe = counting
        try:
            errors = check_dependencies(self.root)
        finally:
            checker.load_recipe = original

        self.assertEqual(errors, [])
        self.assertEqual(len(calls), 2, "each recipe must be parsed once")


class TestCliIsCwdIndependent(unittest.TestCase):
    """The checker must not silently pass when run outside the repo root."""

    def test_runs_from_unrelated_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(REPO_ROOT / "check_dependencies.py")],
                cwd=tmp, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("All dependencies resolve", result.stdout)
        count = int(result.stdout.split("(")[1].split()[0])
        self.assertGreater(count, 100)

    def test_cli_refuses_to_pass_on_empty_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "empty_check.py"
            script.write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
                "from pathlib import Path\n"
                "from check_dependencies import check_dependencies\n"
                f"sys.exit(1 if check_dependencies(Path({tmp!r})) else 0)\n"
            )
            result = subprocess.run(
                [sys.executable, str(script)], capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 1)


class TestMainWalksTheTreeOnce(unittest.TestCase):
    """main() must not re-walk the tree to count recipes."""

    def test_main_walks_the_tree_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_recipe(root, "zlib", "zlib", [])
            with unittest.mock.patch(
                "check_dependencies.recipe_files", wraps=recipe_files
            ) as walk:
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    status = main(root)
        self.assertEqual(status, 0)
        self.assertEqual(walk.call_count, 1)
        self.assertIn("(1 recipe)", out.getvalue())


class TestRealRepository(unittest.TestCase):
    """Guards the invariant on the actual recipe tree."""

    def test_all_dependencies_resolve(self):
        errors = check_dependencies(RECIPES_DIR)
        if errors:
            self.fail(
                "Unresolved dependencies:\n"
                + "\n".join(f"  {e}" for e in errors)
            )

    def test_no_alias_collisions_in_real_tree(self):
        collect_recipes(RECIPES_DIR)  # raises AliasCollision on conflict


class TestHostTools(unittest.TestCase):
    def test_host_tools_are_lowercase(self):
        for tool in HOST_TOOLS:
            self.assertEqual(tool, tool.lower(), tool)

    def test_host_tools_have_no_recipes(self):
        # A host tool that also has a recipe would make the exemption dead.
        self.assertEqual(set(collect_recipes(RECIPES_DIR)) & set(HOST_TOOLS), set())


if __name__ == "__main__":
    unittest.main()


class TestMalformedDependenciesReportCleanly(unittest.TestCase):
    """A string-typed dependencies field must not surface as a traceback.

    make site deliberately skips the checkers, so a recipe with a malformed
    field reaches the generators directly. Every entry point that can see the
    problem has to report it the same way.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def make_bad_recipe(self):
        d = self.root / "z" / "zlib"
        d.mkdir(parents=True)
        (d / "library.toml").write_text(
            'title = "zlib"\n'
            'version = "1.3.1"\n'
            'description = "Test."\n'
            'license = "zlib"\n'
            'canonical_name = "zlib"\n'
            'recipe_url = "https://example.com/z.tar.gz"\n'
            'output_type = "library"\n'
            'dependencies = "None"\n'
        )
        (d / "install.sh").write_text("#!/bin/bash\nset -e\n")
        return d

    def test_library_raises_a_type_error_naming_the_field(self):
        from check_dependencies import collect_entries

        self.make_bad_recipe()
        with self.assertRaises(TypeError) as ctx:
            collect_entries(self.root)
        self.assertIn("dependencies", str(ctx.exception))

    def test_helper_raises_type_error_for_malformed_deps(self):
        # The private helper must raise, not report, a malformed field.
        self.make_bad_recipe()
        with self.assertRaises(TypeError):
            _check_dependencies(self.root)

    def test_cli_reports_the_field_without_a_traceback(self):
        from check_dependencies import main

        self.make_bad_recipe()
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            status = main(base_dir=self.root)

        output = stderr.getvalue()
        self.assertEqual(status, 1)
        self.assertNotIn("Traceback", output)
        self.assertIn("dependencies", output)
