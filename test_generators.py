#!/usr/bin/env python3
"""Tests for the two site generators.

These are the primary artifact of the build: generate_mdbook_src.py produces
the markdown mdBook turns into the published site, and generate_packages.py
produces the machine-readable catalog. Both were previously untested, so a
regression in either would only surface after publishing.
"""

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

import shutil
import stat
import subprocess

import generate_mdbook_src
import generate_packages
from recipe_metadata import RECIPES_DIR, recipe_files, recipe_usage
from recipe_script import TEMPLATE_PREAMBLE, render_install_script

LIB = {
    "title": "Zlib",
    "version": "1.3.1",
    "description": "Compression library.",
    "license": "zlib",
    "canonical_name": "zlib",
    "recipe_url": "https://example.com/zlib.tar.gz",
    "output_type": "library",
}


def lib(**overrides):
    return {**LIB, **overrides}


class TestRecipePage(unittest.TestCase):
    def page(self, **overrides):
        entry = {
            "name": "zlib",
            "title": "Zlib",
            "canonical_name": "zlib",
            "version": "1.3.1",
            "description": "Compression library.",
            "license": "zlib",
            "dependencies": {},
            "recipe_url": "https://example.com/zlib.tar.gz",
            "output_type": "library",
            "last_updated": "2024-01-01",
            "build_dependencies": {},
            "usage": recipe_usage({"libname": "z"}),
        }
        entry.update(overrides)
        return generate_mdbook_src.generate_recipe_page(entry)

    def test_renders_every_documented_field(self):
        text = self.page()
        self.assertIn("# Zlib", text)
        self.assertIn("`zlib`", text)
        self.assertIn("1.3.1", text)
        self.assertIn("zlib", text)
        self.assertIn("https://example.com/zlib.tar.gz", text)
        self.assertIn("2024-01-01", text)
        self.assertIn("[Download install.sh](install.sh)", text)

    def test_no_dependencies_renders_as_none(self):
        self.assertIn("## Dependencies\n\nNone", self.page())

    def test_dependencies_are_listed_sorted_with_constraints(self):
        text = self.page(dependencies={"zlib": "", "openssl": ">=1.1"})
        self.assertIn("- `openssl` (>=1.1)", text)
        self.assertIn("- `zlib`", text)
        self.assertLess(text.index("`openssl`"), text.index("- `zlib`"))

    def test_constraint_free_dependency_has_no_empty_parenthetical(self):
        text = self.page(dependencies={"zlib": ""})
        self.assertIn("- `zlib`\n", text)

    def test_last_update_is_omitted_when_unknown(self):
        self.assertNotIn("## Last Update", self.page(last_updated=""))

    def test_missing_recipe_url_is_reported_as_not_available(self):
        self.assertIn("N/A", self.page(recipe_url=""))

    def test_build_dependencies_are_listed_apart_from_libraries(self):
        text = self.page(dependencies={"zlib": ""},
                         build_dependencies={"cmake": ""})
        self.assertIn("## Build Dependencies\n\n- `cmake`", text)
        self.assertNotIn("- `cmake`", text.split("## Build Dependencies")[0])

    def test_usage_names_the_link_flags_and_directories(self):
        text = self.page(usage=recipe_usage(
            {"libname": ["avcodec", "avutil"], "include_dir": "include/ff"}))
        self.assertIn("## Usage", text)
        self.assertIn("`-lavcodec -lavutil`", text)
        self.assertIn("`include/ff`", text)
        self.assertIn("`lib`", text)

    def test_usage_of_a_header_only_library_has_no_link_flags(self):
        text = self.page(usage=recipe_usage({"header_only": True}))
        self.assertIn("Header-only", text)
        self.assertNotIn("`-l", text)

    def test_usage_notes_are_rendered(self):
        text = self.page(usage=recipe_usage(
            {"header_only": True, "notes": "Define STB_DS_IMPLEMENTATION."}))
        self.assertIn("Define STB_DS_IMPLEMENTATION.", text)


class TestLetterPage(unittest.TestCase):
    def page(self, libs):
        return generate_mdbook_src.generate_letter_page("Z", libs)

    def test_row_per_recipe_linking_to_its_page(self):
        text = self.page([
            {"name": "zlib", "version": "1.3.1", "license": "zlib",
             "last_updated": "2024-01-01"},
        ])
        self.assertIn("| [zlib](zlib/) | 1.3.1 | zlib | 2024-01-01 |", text)

    def test_total_is_reported(self):
        text = self.page([
            {"name": "zlib", "version": "1.3.1", "license": "zlib", "last_updated": ""},
            {"name": "zstd", "version": "1.5.6", "license": "BSD", "last_updated": ""},
        ])
        self.assertIn("**Total: 2 packages starting with Z**", text)

    def test_pipe_in_metadata_does_not_break_the_table(self):
        # A license string is free text; a stray pipe would otherwise split one
        # table row into two and corrupt the rendered page.
        text = self.page([
            {"name": "weird", "version": "1.0", "license": "MIT | BSD",
             "last_updated": ""},
        ])
        rows = [ln for ln in text.splitlines()
                if ln.startswith("|") and "weird" in ln]
        self.assertEqual(len(rows), 1)
        self.assertIn("MIT \\| BSD", rows[0])

    def test_newline_in_metadata_does_not_break_the_table(self):
        # TOML permits \n in a string; a license containing one would split a
        # single table row into two lines and corrupt the rendered page.
        text = self.page([
            {"name": "weird", "version": "1.0", "license": "MIT\nand BSD",
             "last_updated": ""},
        ])
        rows = [ln for ln in text.splitlines()
                if ln.startswith("|") and "weird" in ln]
        self.assertEqual(len(rows), 1)
        self.assertIn("MIT and BSD", rows[0])


class TestSummary(unittest.TestCase):
    def test_letters_and_recipes_are_ordered_and_indented(self):
        text = generate_mdbook_src.generate_summary({
            "Z": [{"name": "zstd"}, {"name": "zlib"}],
            "A": [{"name": "acl"}],
        })
        self.assertLess(text.index("](a/index.md)"), text.index("](z/index.md)"))
        # Within a letter, recipes are alphabetical, nested under the letter.
        self.assertLess(text.index("zlib/index.md"), text.index("zstd/index.md"))
        self.assertIn("    - [acl](a/acl/index.md)", text)
        self.assertIn("[Home](index.md)", text)

    def test_real_tree_summary_covers_every_recipe(self):
        summary = generate_mdbook_src.generate_summary(
            generate_mdbook_src.load_recipes()
        )
        for toml_file in recipe_files(RECIPES_DIR):
            entry = f"/{toml_file.parent.name}/index.md"
            with self.subTest(recipe=toml_file.parent.name):
                self.assertIn(entry, summary)


class TestPackages(unittest.TestCase):
    def test_json_path_mirrors_the_html_page_path(self):
        path = generate_packages.recipe_json_path(
            RECIPES_DIR / "e" / "exif" / "library.toml", "libexif"
        )
        self.assertEqual(path.parts[-3:], ("e", "exif", "libexif.json"))

    def test_json_path_honours_an_explicit_docs_root(self):
        path = generate_packages.recipe_json_path(
            RECIPES_DIR / "z" / "zlib" / "library.toml", "Zlib",
            Path("/srv/out"),
        )
        self.assertTrue(str(path).startswith("/srv/out/"))

    def test_version_data_carries_the_documented_fields(self):
        data = generate_packages.version_data(
            RECIPES_DIR / "z" / "zlib" / "library.toml", lib()
        )
        self.assertEqual(
            set(data),
            {"version", "canonical_name", "description", "license",
             "dependencies", "build_dependencies", "recipe_url",
             "output_type", "last_updated", "libname", "header_only",
             "include_dir", "lib_dir", "notes"},
        )
        self.assertEqual(data["dependencies"], {})

    def test_version_data_normalizes_the_usage_fields(self):
        data = generate_packages.version_data(
            RECIPES_DIR / "z" / "zlib" / "library.toml", lib(libname="z"))
        self.assertEqual(data["libname"], ["z"])
        self.assertIs(data["header_only"], False)
        self.assertEqual(data["include_dir"], "include")
        self.assertEqual(data["lib_dir"], "lib")
        self.assertEqual(data["notes"], "")

    def test_version_data_keeps_explicit_usage_fields(self):
        data = generate_packages.version_data(
            RECIPES_DIR / "z" / "zlib" / "library.toml",
            lib(header_only=True, include_dir="include/stb", notes="n"))
        self.assertEqual(data["libname"], [])
        self.assertIs(data["header_only"], True)
        self.assertEqual(data["include_dir"], "include/stb")
        self.assertEqual(data["notes"], "n")

    def test_version_data_separates_build_dependencies(self):
        data = generate_packages.version_data(
            RECIPES_DIR / "z" / "zstd" / "library.toml",
            lib(**{"build-dependencies": {"cmake": ""}}))
        self.assertEqual(data["build_dependencies"], {"cmake": ""})
        self.assertEqual(data["dependencies"], {})

    def test_version_data_normalizes_dependencies(self):
        data = generate_packages.version_data(
            RECIPES_DIR / "z" / "zlib" / "library.toml",
            lib(dependencies={"openssl": ">=1.1"}),
        )
        self.assertEqual(data["dependencies"], {"openssl": ">=1.1"})

    def test_main_writes_one_json_per_recipe_plus_the_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            # main() returns an exit code, not a count, so the recipe total is
            # read back off disk instead.
            self.assertEqual(generate_packages.main(docs_dir=docs), 0)

            index = json.loads(
                (docs / ".well-known" / "packages.json").read_text()
            )
            self.assertGreater(len(index), 100)
            per_recipe_files = list(docs.glob("*/*/*.json"))
            self.assertEqual(len(per_recipe_files), len(index))

            # The aggregate entry carries the recipe fields flattened, the
            # per-recipe file carries them under a versions list.
            zlib = next(e for e in index if e["name"] == "zlib")
            self.assertEqual(zlib["canonical_name"], "zlib")

            per_recipe = json.loads((docs / "z" / "zlib" / "zlib.json").read_text())
            self.assertEqual(per_recipe["name"], "zlib")
            self.assertEqual(len(per_recipe["versions"]), 1)
            self.assertEqual(zlib["version"], per_recipe["versions"][0]["version"])

    def test_nothing_is_written_into_the_working_directory(self):
        # Run from an empty directory: both output roots are absolute, so a
        # relative-path regression would scatter files into the cwd. The cwd is
        # restored in a finally block rather than via addCleanup, so it goes
        # back before any assertion failure is reported.
        with tempfile.TemporaryDirectory() as tmp:
            origin = Path.cwd()
            try:
                os.chdir(tmp)
                with tempfile.TemporaryDirectory() as out:
                    self.assertEqual(
                        generate_packages.main(docs_dir=Path(out)), 0
                    )
                leftovers = sorted(p.name for p in Path(tmp).iterdir())
            finally:
                os.chdir(origin)
        self.assertEqual(leftovers, [])


TEMPLATE = TEMPLATE_PREAMBLE + 'echo "$PACKAGE|$VERSION|$URL|$PREFIX"\n'


class TestInstallScriptRendering(unittest.TestCase):
    """The published install.sh is the repo template plus a generated header.

    library.toml is the one place that names the version and URL; the template
    only reads $PACKAGE, $VERSION, $URL and $PREFIX.
    """

    def setUp(self):
        if shutil.which("bash") is None:
            self.skipTest("bash is not installed")
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def run_rendered(self, data, *args, template=TEMPLATE):
        script = self.root / "install.sh"
        script.write_text(render_install_script(template, data))
        env = {**os.environ, "COFFEE_HOME": str(self.root / "coffee"),
               "TMPDIR": str(self.root)}
        return subprocess.run(["bash", str(script), *args], cwd=self.root,
                              capture_output=True, text=True, env=env)

    def test_header_takes_name_version_and_url_from_the_recipe(self):
        result = self.run_rendered(lib())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            f"zlib|1.3.1|https://example.com/zlib.tar.gz|"
            f"{self.root}/coffee/zlib/1.3.1",
        )

    def test_package_is_the_canonical_name_not_the_title(self):
        result = self.run_rendered(lib(title="Zlib", canonical_name="z_lib"))
        self.assertTrue(result.stdout.startswith("z_lib|"), result.stdout)

    def test_first_argument_overrides_the_prefix(self):
        result = self.run_rendered(lib(), "/opt/zlib")
        self.assertTrue(result.stdout.strip().endswith("|/opt/zlib"))

    def test_a_relative_prefix_is_made_absolute(self):
        # The body runs in a scratch directory, so a relative prefix would
        # otherwise install into it and be deleted on exit.
        result = self.run_rendered(lib(), "relative/dir")
        self.assertTrue(
            result.stdout.strip().endswith(f"|{self.root}/relative/dir"),
            result.stdout)

    def test_body_runs_in_a_scratch_directory_removed_on_exit(self):
        result = self.run_rendered(
            lib(), template=TEMPLATE_PREAMBLE + "pwd\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        scratch = Path(result.stdout.strip())
        self.assertNotEqual(scratch, self.root)
        self.assertTrue(scratch.is_relative_to(self.root))
        self.assertFalse(scratch.exists())

    def test_metadata_is_quoted_not_executed(self):
        evil = 'x"; touch pwned; echo "'
        result = self.run_rendered(lib(version=evil, recipe_url="$(id)"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"|{evil}|$(id)|", result.stdout)
        self.assertFalse((self.root / "pwned").exists())

    def test_template_must_start_with_the_preamble(self):
        with self.assertRaisesRegex(ValueError, "set -e -o pipefail -u"):
            render_install_script("#!/bin/bash\necho hi\n", lib())

    def test_template_may_not_assign_a_header_variable(self):
        for var in ("PACKAGE", "VERSION", "URL", "PREFIX", "COFFEE_HOME",
                    "WORK"):
            with self.subTest(var=var):
                with self.assertRaisesRegex(ValueError, var):
                    render_install_script(
                        TEMPLATE_PREAMBLE + f'{var}="x"\n', lib())

    def test_main_publishes_the_rendered_script_executable(self):
        out = self.root / "src"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(generate_mdbook_src.main(src_dir=out), 0)
        published = out / "z" / "zlib" / "install.sh"
        text = published.read_text()
        self.assertIn("\nVERSION=", text)
        self.assertIn("\nURL=", text)
        self.assertTrue(published.stat().st_mode & stat.S_IXUSR)


class TestGeneratorPathsAreAbsolute(unittest.TestCase):
    """Running a generator from a subdirectory must not scatter output."""

    def test_src_dir_is_under_the_repository(self):
        self.assertTrue(generate_mdbook_src.SRC_DIR.is_absolute())

    def test_docs_dir_is_under_the_repository(self):
        self.assertTrue(generate_packages.DOCS_DIR.is_absolute())


if __name__ == "__main__":
    unittest.main()


class TestMalformedRecipeFailsCleanly(unittest.TestCase):
    """`make site` skips the checkers, so a generator must not crash on bad metadata.

    A string-typed dependencies field raises TypeError out of
    parse_dependencies. The checkers catch it; the generators have to as well,
    or a rebuild without the checks dies with a stack trace instead of a
    one-line message naming the recipe.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.bad = self.root / "z" / "zlib"
        self.bad.mkdir(parents=True)
        (self.bad / "library.toml").write_text(
            'title = "zlib"\n'
            'version = "1.3.1"\n'
            'description = "Test."\n'
            'license = "zlib"\n'
            'canonical_name = "zlib"\n'
            'recipe_url = "https://example.com/z.tar.gz"\n'
            'output_type = "library"\n'
            'dependencies = "None"\n'
        )
        (self.bad / "install.sh").write_text("#!/bin/bash\nset -e\n")

    def run_quietly(self, call, *args, **kwargs):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            status = call(*args, **kwargs)
        return status, stderr.getvalue()

    def test_mdbook_generator_reports_the_recipe_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as out:
            src = Path(out) / "src"
            status, err = self.run_quietly(
                generate_mdbook_src.main, recipes_dir=self.root, src_dir=src
            )
        self.assertEqual(status, 1)
        self.assertNotIn("Traceback", err)
        self.assertIn("dependencies", err)
        self.assertIn("zlib", err)

    def test_packages_generator_reports_the_recipe_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as out:
            status, err = self.run_quietly(
                generate_packages.main,
                recipes_dir=self.root, docs_dir=Path(out),
            )
        self.assertEqual(status, 1)
        self.assertNotIn("Traceback", err)
        self.assertIn("dependencies", err)

    def test_a_valid_tree_still_succeeds(self):
        # Guards against the handler swallowing everything.
        with tempfile.TemporaryDirectory() as out:
            status, _ = self.run_quietly(
                generate_packages.main,
                recipes_dir=RECIPES_DIR, docs_dir=Path(out),
            )
        self.assertEqual(status, 0)

    def test_mdbook_generator_reports_a_bad_template_without_a_traceback(self):
        (self.bad / "library.toml").write_text(
            (self.bad / "library.toml").read_text()
            .replace('dependencies = "None"', 'libname = "z"\n[dependencies]'))
        (self.bad / "install.sh").write_text(
            '#!/bin/bash\nset -e -o pipefail -u\nVERSION="1"\n')
        with tempfile.TemporaryDirectory() as out:
            status, err = self.run_quietly(
                generate_mdbook_src.main, recipes_dir=self.root,
                src_dir=Path(out) / "src")
        self.assertEqual(status, 1)
        self.assertNotIn("Traceback", err)
        self.assertIn("zlib", err)
        self.assertIn("VERSION", err)

    def make_syntax_bad_recipe(self):
        (self.bad / "library.toml").write_text('title = "unterminated\n')
        (self.bad / "install.sh").write_text("#!/bin/bash\nset -e\n")

    def test_mdbook_generator_reports_a_syntax_error_without_a_traceback(self):
        self.make_syntax_bad_recipe()
        with tempfile.TemporaryDirectory() as out:
            src = Path(out) / "src"
            status, err = self.run_quietly(
                generate_mdbook_src.main, recipes_dir=self.root, src_dir=src
            )
        self.assertEqual(status, 1)
        self.assertNotIn("Traceback", err)
        self.assertIn("zlib", err)

    def test_packages_generator_reports_a_syntax_error_without_a_traceback(self):
        self.make_syntax_bad_recipe()
        with tempfile.TemporaryDirectory() as out:
            status, err = self.run_quietly(
                generate_packages.main,
                recipes_dir=self.root, docs_dir=Path(out),
            )
        self.assertEqual(status, 1)
        self.assertNotIn("Traceback", err)
        self.assertIn("zlib", err)
