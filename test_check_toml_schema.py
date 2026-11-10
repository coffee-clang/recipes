#!/usr/bin/env python3
"""Tests for the recipe TOML schema checker.

The CLI tests exist because this checker used to report "All 0 TOML files are
valid" and exit 0 when run from outside the repository root: it resolved the
recipe tree with a relative Path("recipes"). A vacuous pass is worse than a
crash, so the cwd requirement and the empty-tree refusal are both pinned.
"""

import contextlib
import io
import re
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

from check_toml_schema import check_toml_schemas, main
from recipe_metadata import RECIPES_DIR, load_recipe, recipe_files

REPO_ROOT = Path(__file__).resolve().parent


def write_toml(root, name, *, output_type="library", omit=(), extra=""):
    """Write a minimal valid recipe.

    Scalar keys first, then `extra`. `dependencies` defaults to an empty
    ``[dependencies]`` table; omit it to supply a different spelling.
    """
    d = root / name[0] / name
    d.mkdir(parents=True)
    fields = {
        "title": f'"{name}"',
        "version": '"1.0.0"',
        "description": '"Test."',
        "license": '"MIT"',
        "recipe_url": '"https://example.com/x.git"',
        "canonical_name": f'"{name}"',
        "output_type": f'"{output_type}"',
        "libname": f'"{name}"',
        "sha256": f'"{"ab" * 32}"',
        "sha256_source": '"upstream"',
    }
    # `extra` goes before the [dependencies] header: in TOML, a key written
    # after a table header belongs to that table, not to the root.
    lines = [f"{k} = {v}" for k, v in fields.items() if k not in omit]
    lines.append(extra)
    if "dependencies" not in omit:
        lines.append("[dependencies]")
    (d / "library.toml").write_text("\n".join(lines) + "\n")
    (d / "install.sh").write_text("#!/bin/bash\nset -e\n")
    return d


class TestValidRecipes(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_valid_recipe_passes(self):
        write_toml(self.root, "zlib")
        self.assertEqual(check_toml_schemas(self.root), [])

    def test_table_dependencies_pass(self):
        write_toml(self.root, "curl", omit=("dependencies",),
                   extra='[dependencies]\nzlib = ""\n')
        self.assertEqual(check_toml_schemas(self.root), [])

    def test_empty_dependency_table_passes(self):
        # The only spelling of "no dependencies"; recipes/x/xorgproto uses it.
        write_toml(self.root, "xorgproto", omit=("dependencies",),
                   extra="[dependencies]\n")
        self.assertEqual(check_toml_schemas(self.root), [])

    def test_all_three_output_types_pass(self):
        for i, output_type in enumerate(("library", "executable", "both")):
            write_toml(self.root, f"pkg{i}", output_type=output_type)
        self.assertEqual(check_toml_schemas(self.root), [])


class TestUsageFields(unittest.TestCase):
    """How a consumer uses the installed library (R4).

    coffee links with -l<libname> and adds include_dir / lib_dir under the
    prefix, so a library recipe that leaves both libname and header_only unset
    gives it nothing to link.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def errors(self, extra, omit=(), output_type="library"):
        write_toml(self.root, "zlib", extra=extra, omit=omit,
                   output_type=output_type)
        return check_toml_schemas(self.root)

    def test_all_usage_fields_pass(self):
        self.assertEqual(self.errors(
            'include_dir = "include/zlib"\nlib_dir = "lib"\n'
            'notes = "Link with -lz."\n'), [])

    def test_libname_may_be_a_list(self):
        self.assertEqual(self.errors('libname = ["avcodec", "avutil"]\n',
                                     omit=("libname",)), [])

    def test_libname_must_be_a_string_or_list_of_strings(self):
        for value in ("1", "[]", '["z", 1]', '[""]', "true"):
            with self.subTest(value=value):
                tree = self.root / f"t{len(list(self.root.iterdir()))}"
                tree.mkdir()
                write_toml(tree, "zlib", omit=("libname",),
                           extra=f"libname = {value}\n")
                errors = check_toml_schemas(tree)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("libname", errors[0])

    def test_header_only_passes_without_libname(self):
        self.assertEqual(self.errors("header_only = true\n",
                                     omit=("libname",)), [])

    def test_header_only_must_be_a_boolean(self):
        errors = self.errors('header_only = "yes"\n', omit=("libname",))
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("header_only", errors[0])

    def test_header_only_contradicts_libname(self):
        errors = self.errors("header_only = true\n")
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("header_only", errors[0])
        self.assertIn("libname", errors[0])

    def test_library_needs_libname_or_header_only(self):
        for output_type in ("library", "both"):
            with self.subTest(output_type=output_type):
                tree = self.root / output_type
                tree.mkdir()
                write_toml(tree, "zlib", omit=("libname",),
                           output_type=output_type)
                errors = check_toml_schemas(tree)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("libname", errors[0])

    def test_data_package_needs_neither(self):
        # Protocol descriptions (xcb-proto, wayland-protocols) install files
        # other builds read, with nothing to link or include.
        self.assertEqual(self.errors("", omit=("libname",),
                                     output_type="data"), [])

    def test_executable_needs_neither(self):
        self.assertEqual(self.errors("", omit=("libname",),
                                     output_type="executable"), [])

    def test_directories_must_be_relative_paths_inside_the_prefix(self):
        for field in ("include_dir", "lib_dir"):
            for value in ('"/usr/include"', '"../include"', '""', "1"):
                with self.subTest(field=field, value=value):
                    tree = self.root / f"t{len(list(self.root.iterdir()))}"
                    tree.mkdir()
                    write_toml(tree, "zlib", extra=f"{field} = {value}\n")
                    errors = check_toml_schemas(tree)
                    self.assertEqual(len(errors), 1, errors)
                    self.assertIn(field, errors[0])

    def test_notes_must_be_a_string(self):
        errors = self.errors("notes = 1\n")
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("notes", errors[0])

    def test_build_dependencies_must_be_a_table(self):
        write_toml(self.root, "zstd",
                   extra='"build-dependencies" = "cmake"\n')
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("[build-dependencies]", errors[0])

    def test_build_dependencies_table_passes(self):
        d = write_toml(self.root, "zstd")
        toml = d / "library.toml"
        toml.write_text(toml.read_text() + '[build-dependencies]\ncmake = ""\n')
        self.assertEqual(check_toml_schemas(self.root), [])


class TestDigestFields(unittest.TestCase):
    """The published script verifies the download against sha256."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def errors(self, field, value):
        tree = self.root / f"t{len(list(self.root.iterdir()))}"
        tree.mkdir()
        write_toml(tree, "zlib", omit=(field,), extra=f"{field} = {value}\n")
        return check_toml_schemas(tree)

    def test_sha256_must_be_64_lowercase_hex_digits(self):
        for value in ('"abc"', f'"{"AB" * 32}"', f'"{"zz" * 32}"',
                      f'"{"ab" * 32}0"', "1"):
            with self.subTest(value=value):
                errors = self.errors("sha256", value)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("sha256", errors[0])

    def test_every_digest_source_is_accepted(self):
        for value in ("upstream", "signature", "tofu"):
            with self.subTest(value=value):
                self.assertEqual(self.errors("sha256_source", f'"{value}"'),
                                 [])

    def test_unknown_digest_source_is_rejected(self):
        errors = self.errors("sha256_source", '"guess"')
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("sha256_source", errors[0])


class TestMissingFields(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_every_mandatory_field_is_required(self):
        for field in ("title", "version", "description", "license",
                      "recipe_url", "canonical_name", "output_type",
                      "dependencies", "sha256", "sha256_source"):
            with self.subTest(field=field):
                # A per-field tree, so one field's omission is the only error.
                tree = self.root / field
                tree.mkdir()
                write_toml(tree, "zlib", omit=(field,))
                errors = check_toml_schemas(tree)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(field, errors[0])

    def test_blank_string_counts_as_missing(self):
        write_toml(self.root, "zlib", omit=("license",),
                   extra='license = ""')
        # A blank license is present but empty, so it must still be reported.
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("license", errors[0])


class TestInvalidValues(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_unknown_output_type_is_rejected(self):
        write_toml(self.root, "zlib", output_type="static-lib")
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("output_type", errors[0])
        self.assertIn("static-lib", errors[0])

    def test_string_dependencies_are_rejected(self):
        # The old parser split strings on whitespace, so dependencies = "None"
        # became three packages named None, of and these. The form is gone.
        write_toml(self.root, "xorgproto", omit=("dependencies",),
                   extra='dependencies = "None"\n')
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("dependencies", errors[0])
        self.assertIn("table", errors[0])

    def test_comma_separated_string_dependencies_are_rejected(self):
        write_toml(self.root, "curl", omit=("dependencies",),
                   extra='dependencies = "zlib, openssl"\n')
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("dependencies", errors[0])

    def test_malformed_toml_is_reported_not_raised(self):
        d = write_toml(self.root, "zlib")
        (d / "library.toml").write_text("title = 'unterminated\n")
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("zlib", errors[0])

    def test_invalid_utf8_is_reported_not_raised(self):
        # tomllib decodes the file itself, so invalid UTF-8 raises
        # UnicodeDecodeError, a sibling of TOMLDecodeError under ValueError.
        # It must land in errors like any other unreadable recipe.
        d = write_toml(self.root, "zlib")
        (d / "library.toml").write_bytes(b"\xff\xfe")
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("zlib", errors[0])
        self.assertIn("unreadable recipe", errors[0])


class TestTitlePathSafety(unittest.TestCase):
    """The title becomes a filename in generate_packages.py.

    A title containing a path separator would write the recipe JSON outside its
    own directory, so the schema pins the character set instead of relying on
    every future author to remember.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_separator_in_title_is_rejected(self):
        write_toml(self.root, "evil", omit=("title",),
                   extra='title = "../../etc/passwd"')
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("title", errors[0])

    def test_plain_title_with_spaces_and_dots_is_accepted(self):
        # "libjpeg-turbo 2.0" is the shape real titles take, and the two dots
        # in "2.0" must not be mistaken for a traversal.
        write_toml(self.root, "ok", omit=("title",),
                   extra='title = "libjpeg-turbo 2.0"')
        self.assertEqual(check_toml_schemas(self.root), [])

    def test_real_titles_are_all_path_safe(self):
        for toml_file in recipe_files(RECIPES_DIR):
            title = load_recipe(toml_file).get("title", "")
            with self.subTest(recipe=toml_file.parent.name):
                self.assertNotIn("/", title)
                self.assertNotIn("\\", title)


class TestEmptyTree(unittest.TestCase):
    """The regression guard for the guard: a vacuous pass must not be possible."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_empty_tree_refuses_to_report_success(self):
        errors = check_toml_schemas(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("refusing to report success", errors[0])

    def test_missing_directory_refuses_to_report_success(self):
        errors = check_toml_schemas(self.root / "nope")
        self.assertEqual(len(errors), 1)
        self.assertIn("refusing to report success", errors[0])


class TestCliIsCwdIndependent(unittest.TestCase):
    """The checker must not silently pass when run outside the repo root."""

    def test_runs_from_unrelated_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(REPO_ROOT / "check_toml_schema.py")],
                cwd=tmp, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TOML files are valid", result.stdout)
        count = int(re.search(r"All (\d+) TOML", result.stdout).group(1))
        self.assertGreater(count, 100)

    def test_cli_fails_from_unrelated_cwd_on_empty_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "empty_check.py"
            script.write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
                "from pathlib import Path\n"
                "from check_toml_schema import check_toml_schemas\n"
                f"sys.exit(1 if check_toml_schemas(Path({tmp!r})) else 0)\n"
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
            write_toml(root, "zlib")
            with unittest.mock.patch(
                "check_toml_schema.recipe_files", wraps=recipe_files
            ) as walk:
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    status = main(root)
        self.assertEqual(status, 0)
        self.assertEqual(walk.call_count, 1)
        self.assertIn("1 TOML file is valid", out.getvalue())


class TestRealRepository(unittest.TestCase):
    """Guards the invariant on the actual recipe tree."""

    def test_all_recipes_are_valid(self):
        errors = check_toml_schemas(RECIPES_DIR)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_output_types_are_from_the_documented_set(self):
        self.assertGreater(len(list(RECIPES_DIR.rglob("library.toml"))), 100)


if __name__ == "__main__":
    unittest.main()