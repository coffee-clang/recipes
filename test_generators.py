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

import generate_mdbook_src
import generate_packages
from recipe_metadata import RECIPES_DIR, recipe_files

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
             "dependencies", "recipe_url", "output_type", "last_updated"},
        )
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
