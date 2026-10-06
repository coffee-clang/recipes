#!/usr/bin/env python3
import io
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from check_canonical_names import (
    check_canonical_names,
    is_valid_canonical_name,
    main,
)
from recipe_metadata import RECIPES_DIR

REPO_ROOT = Path(__file__).resolve().parent


def make_recipe(root, name, canonical_name=None):
    d = root / name[0] / name
    d.mkdir(parents=True)
    lines = [
        f'title = "{name}"',
        'version = "1.0.0"',
        'description = "Test."',
        'license = "MIT"',
        'recipe_url = "https://example.com/x.git"',
        'output_type = "library"',
    ]
    if canonical_name is not None:
        lines.append(f'canonical_name = "{canonical_name}"')
    (d / "library.toml").write_text("\n".join(lines) + "\n")
    (d / "install.sh").write_text("#!/bin/bash\n")
    return d


class TestIsValidCanonicalName(unittest.TestCase):
    def test_underscore_names_are_valid(self):
        for name in ("zlib", "libjpeg_turbo", "util_linux", "alsa_lib", "_x", "a1"):
            with self.subTest(name=name):
                self.assertTrue(is_valid_canonical_name(name))

    def test_dash_in_canonical_name_fails(self):
        self.assertFalse(is_valid_canonical_name("libjpeg-turbo"))

    def test_dot_and_space_fail(self):
        for name in ("lib.jpeg", "lib jpeg", "lib.jpeg.turbo"):
            with self.subTest(name=name):
                self.assertFalse(is_valid_canonical_name(name))

    def test_leading_digit_fails(self):
        self.assertFalse(is_valid_canonical_name("7zip"))

    def test_empty_fails(self):
        self.assertFalse(is_valid_canonical_name(""))

    def test_non_ascii_fails(self):
        # isalnum() is true for many unicode letters, which are not valid in a
        # C identifier.
        self.assertFalse(is_valid_canonical_name("libnaïve"))


class TestCheckCanonicalNames(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_valid_names_pass(self):
        make_recipe(self.root, "zlib", "zlib")
        make_recipe(self.root, "jpeg", "libjpeg_turbo")
        duplicates, invalid, tree_errors, count = check_canonical_names(self.root)
        self.assertEqual(duplicates, [])
        self.assertEqual(invalid, [])
        self.assertEqual(tree_errors, [])
        self.assertEqual(count, 2)

    def test_duplicate_canonical_name_reported(self):
        make_recipe(self.root, "zlib", "zlib")
        make_recipe(self.root, "zlibcopy", "zlib")
        duplicates, invalid, tree_errors, count = check_canonical_names(self.root)
        self.assertEqual(len(duplicates), 1)
        self.assertIn("zlib", duplicates[0])
        self.assertEqual(tree_errors, [])
        self.assertEqual(count, 2)

    def test_dash_in_canonical_name_reported_with_suggestion(self):
        make_recipe(self.root, "jpeg", "libjpeg-turbo")
        duplicates, invalid, tree_errors, count = check_canonical_names(self.root)
        self.assertEqual(len(invalid), 1)
        self.assertIn("libjpeg-turbo", invalid[0])
        self.assertIn("libjpeg_turbo", invalid[0])
        self.assertEqual(tree_errors, [])
        self.assertEqual(count, 1)

    def test_directory_name_is_used_when_canonical_name_absent(self):
        # recipes/e/exif/ is titled libexif; the directory supplies the name.
        make_recipe(self.root, "jpeg-turbo", None)
        duplicates, invalid, tree_errors, count = check_canonical_names(self.root)
        self.assertEqual(len(invalid), 1)
        self.assertIn("jpeg-turbo", invalid[0])
        self.assertEqual(tree_errors, [])
        self.assertEqual(count, 1)

    def test_malformed_recipe_is_reported_not_raised(self):
        # A library.toml that fails to parse must be reported as a tree-level
        # failure, not traceback out of the checker.
        d = make_recipe(self.root, "zlib", "zlib")
        (d / "library.toml").write_text('title = "unterminated\n')
        duplicates, invalid, tree_errors, count = check_canonical_names(self.root)
        self.assertEqual(duplicates, [])
        self.assertEqual(invalid, [])
        self.assertEqual(len(tree_errors), 1)
        self.assertIn("zlib", tree_errors[0])
        self.assertEqual(count, 1)

    def test_result_exposes_named_fields(self):
        make_recipe(self.root, "zlib", "zlib")
        make_recipe(self.root, "jpeg", "libjpeg_turbo")
        result = check_canonical_names(self.root)
        self.assertEqual(result.duplicates, [])
        self.assertEqual(result.invalid, [])
        self.assertEqual(result.tree_errors, [])
        self.assertEqual(result.count, 2)
        # A NamedTuple still unpacks positionally, so existing call sites hold.
        duplicates, invalid, tree_errors, count = result
        self.assertEqual(count, 2)


class TestEmptyTree(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_empty_tree_refuses_to_report_success(self):
        duplicates, invalid, tree_errors, count = check_canonical_names(self.root)
        self.assertEqual(duplicates, [])
        self.assertEqual(invalid, [])
        self.assertEqual(len(tree_errors), 1)
        self.assertIn("refusing to report success", tree_errors[0])
        self.assertEqual(count, 0)

    def test_missing_directory_refuses_to_report_success(self):
        duplicates, invalid, tree_errors, count = check_canonical_names(
            self.root / "nope")
        self.assertEqual(duplicates, [])
        self.assertEqual(invalid, [])
        self.assertEqual(len(tree_errors), 1)
        self.assertIn("refusing to report success", tree_errors[0])
        self.assertEqual(count, 0)


class TestMainLabelsRefusal(unittest.TestCase):
    """The empty-tree refusal is a tree failure, not an invalid name."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_main_labels_the_refusal_as_a_tree_failure(self):
        with redirect_stderr(io.StringIO()) as err:
            status = main(self.root)
        self.assertEqual(status, 1)
        self.assertIn("refusing to report success", err.getvalue())
        self.assertNotIn("Invalid canonical names found:", err.getvalue())

    def test_main_reports_invalid_names_under_their_own_header(self):
        make_recipe(self.root, "jpeg", "libjpeg-turbo")
        with redirect_stderr(io.StringIO()) as err:
            status = main(self.root)
        self.assertEqual(status, 1)
        self.assertIn("Invalid canonical names found:", err.getvalue())

    def test_main_reports_a_malformed_recipe_under_the_general_header(self):
        # A parse failure is a tree-level failure, not an invalid name, so it
        # must not appear under the "Invalid canonical names found:" header.
        d = make_recipe(self.root, "zlib", "zlib")
        (d / "library.toml").write_text('title = "unterminated\n')
        with redirect_stderr(io.StringIO()) as err:
            status = main(self.root)
        self.assertEqual(status, 1)
        self.assertIn("unreadable recipe", err.getvalue())
        self.assertNotIn("Invalid canonical names found:", err.getvalue())

    def test_main_succeeds_on_a_valid_tree(self):
        make_recipe(self.root, "zlib", "zlib")
        with redirect_stdout(io.StringIO()) as out:
            status = main(self.root)
        self.assertEqual(status, 0)
        self.assertIn("libraries checked", out.getvalue())


class TestCliIsCwdIndependent(unittest.TestCase):
    """The checker must not silently pass when run outside the repo root."""

    def test_runs_from_unrelated_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(REPO_ROOT / "check_canonical_names.py")],
                cwd=tmp, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("libraries checked", result.stdout)
        count = int(re.search(r"\((\d+) libraries", result.stdout).group(1))
        self.assertGreater(count, 100)

    def test_cli_refuses_to_pass_on_empty_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "empty_check.py"
            script.write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
                "from pathlib import Path\n"
                "from check_canonical_names import main\n"
                f"sys.exit(main(Path({tmp!r})))\n"
            )
            result = subprocess.run(
                [sys.executable, str(script)], capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("refusing to report success", result.stderr)


class TestRealRepository(unittest.TestCase):
    def test_no_dashes_in_real_tree(self):
        duplicates, invalid, tree_errors, _ = check_canonical_names(RECIPES_DIR)
        self.assertEqual(invalid, [], "\n".join(invalid))
        self.assertEqual(tree_errors, [], "\n".join(tree_errors))

    def test_no_duplicates_in_real_tree(self):
        duplicates, _, _, _ = check_canonical_names(RECIPES_DIR)
        self.assertEqual(duplicates, [], "\n".join(duplicates))

    def test_every_recipe_name_is_a_c_identifier(self):
        _, invalid, _, _ = check_canonical_names(RECIPES_DIR)
        for message in invalid:
            with self.subTest(message=message):
                self.fail(message)


if __name__ == "__main__":
    unittest.main()
