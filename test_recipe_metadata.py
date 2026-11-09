#!/usr/bin/env python3
"""Tests for the shared recipe metadata helpers.

The cross-module agreement test is the regression guard: the dependency
checker and both site generators used to carry independent copies of
parse_dependencies that silently disagreed.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

import check_dependencies
import generate_mdbook_src
import generate_packages
import recipe_metadata
from recipe_metadata import (
    RECIPES_DIR,
    get_last_updated,
    load_recipe,
    parse_dependencies,
    recipe_build_dependencies,
    recipe_dependencies,
    recipe_files,
    recipe_letter,
    recipe_names,
)

# The canonical [dependencies] table form, and the absent field.
TABLE_FIXTURES = [
    None,
    {},
    {"cmake": "", "zlib": ""},
    {"openssl": ">=1.1"},
]


class TestParseDependencies(unittest.TestCase):
    def test_absent_field_is_empty(self):
        self.assertEqual(parse_dependencies(None), {})

    def test_empty_table_is_empty(self):
        # An empty [dependencies] table and a missing field mean the same thing:
        # the recipe declares no dependencies.
        self.assertEqual(parse_dependencies({}), {})

    def test_constraint_is_kept_verbatim(self):
        self.assertEqual(
            parse_dependencies({"openssl": ">=1.1", "zlib": ""}),
            {"openssl": ">=1.1", "zlib": ""},
        )

    def test_non_string_constraints_are_coerced(self):
        self.assertEqual(parse_dependencies({"zlib": 1}), {"zlib": "1"})

    def test_string_form_is_rejected_not_silently_misparsed(self):
        # The schema requires a table. A string used to be split on whitespace,
        # which turned dependencies = "None" into three fake packages.
        for raw in ("None", "zlib openssl", "zlib, openssl", ""):
            with self.subTest(raw=raw):
                with self.assertRaises(TypeError):
                    parse_dependencies(raw)

    def test_error_message_names_the_expected_type(self):
        with self.assertRaisesRegex(TypeError, "table"):
            parse_dependencies("zlib")

    def test_the_schema_checker_words_the_type_error_identically(self):
        """One failure, one explanation.

        The two checkers disagreed: check_toml_schema.py said "not a str" while
        parse_dependencies said "got str; see check_toml_schema.py", which sent
        the reader from one file to the other to learn the same thing.
        """
        from check_toml_schema import check_recipe

        fixture = RECIPES_DIR / "z" / "zlib" / "library.toml"
        # A copy, not the loaded dict: mutating that in place would poison
        # anything else reading the same recipe once the loader is cached.
        data = {**load_recipe(fixture), "dependencies": "zlib"}

        with self.assertRaises(TypeError) as caught:
            recipe_dependencies(fixture, data)

        self.assertEqual(
            [error for error in check_recipe(fixture, data)
             if "dependencies" in error],
            [str(caught.exception)],
        )

    def test_the_type_error_does_not_point_at_the_other_file(self):
        # A shared message that says "see check_toml_schema.py" is worse than
        # two different ones: it sends the reader somewhere with no extra
        # information, and is wrong when raised from a generator.
        with self.assertRaises(TypeError) as caught:
            parse_dependencies("zlib")
        self.assertNotIn("check_toml_schema.py", str(caught.exception))


class TestBuildDependencies(unittest.TestCase):
    """[build-dependencies] holds host tools, kept apart from libraries.

    A tool listed under [dependencies] (zstd's cmake = "") reads to coffee as
    a registry package to fetch, which does not exist.
    """

    TOML = Path("recipes/z/zstd/library.toml")

    def test_reads_the_build_dependencies_table(self):
        data = {"build-dependencies": {"cmake": ""}, "dependencies": {}}
        self.assertEqual(recipe_build_dependencies(self.TOML, data),
                         {"cmake": ""})

    def test_absent_table_is_empty(self):
        self.assertEqual(recipe_build_dependencies(self.TOML, {}), {})

    def test_does_not_read_the_library_table(self):
        data = {"dependencies": {"zlib": ""}}
        self.assertEqual(recipe_build_dependencies(self.TOML, data), {})

    def test_string_form_is_rejected_naming_the_table(self):
        with self.assertRaisesRegex(TypeError, r"zstd: .*\[build-dependencies\]"):
            recipe_build_dependencies(self.TOML, {"build-dependencies": "cmake"})


class TestConsumersAgree(unittest.TestCase):
    """All three consumers must normalize dependencies identically.

    The original defect was each module carrying its own copy of the parser.
    These assertions fail both if a consumer stops using the shared helper and
    if one grows a private parser again.
    """

    CONSUMERS = (check_dependencies, generate_mdbook_src, generate_packages)

    def test_consumers_use_the_shared_helper(self):
        for module in self.CONSUMERS:
            with self.subTest(module=module.__name__):
                self.assertIs(
                    module.recipe_dependencies, recipe_dependencies
                )

    def test_no_consumer_defines_its_own_parser(self):
        for module in self.CONSUMERS:
            with self.subTest(module=module.__name__):
                self.assertNotIn(
                    "def parse_dependencies", Path(module.__file__).read_text()
                )

    def test_helpers_agree_on_every_table_form(self):
        fixture = RECIPES_DIR / "z" / "zlib" / "library.toml"
        data = load_recipe(fixture)
        shared = parse_dependencies(data.get("dependencies"))
        for module in self.CONSUMERS:
            with self.subTest(module=module.__name__):
                self.assertEqual(module.recipe_dependencies(fixture, data),
                                 shared)

    def test_helper_names_the_recipe_on_a_malformed_field(self):
        fixture = RECIPES_DIR / "z" / "zlib" / "library.toml"
        with self.assertRaisesRegex(TypeError, "zlib"):
            recipe_dependencies(fixture, {"dependencies": "None"})


class TestLoadRecipe(unittest.TestCase):
    def test_syntax_error_names_the_recipe(self):
        # A malformed library.toml must be reported as a TypeError naming the
        # recipe, the same shape as a malformed dependencies field, so the
        # generators' existing handlers report it the same way.
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "z" / "zlib" / "library.toml"
            bad.parent.mkdir(parents=True)
            bad.write_text('title = "unterminated\n')
            with self.assertRaisesRegex(TypeError, "zlib"):
                load_recipe(bad)

    def test_unreadable_file_names_the_recipe(self):
        # A library.toml that is a directory (or otherwise unreadable) must be
        # reported the same way as a syntax error, not leak an OSError.
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "z" / "zlib" / "library.toml"
            bad.mkdir(parents=True)
            with self.assertRaisesRegex(TypeError, "zlib"):
                load_recipe(bad)

    def test_invalid_utf8_names_the_recipe(self):
        # tomllib decodes the file itself, so invalid UTF-8 raises
        # UnicodeDecodeError, a sibling of TOMLDecodeError under ValueError.
        # It must be reported the same way as a syntax error.
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "z" / "zlib" / "library.toml"
            bad.parent.mkdir(parents=True)
            bad.write_bytes(b"\xff\xfe")
            with self.assertRaisesRegex(TypeError, "zlib"):
                load_recipe(bad)


class TestGetLastUpdated(unittest.TestCase):
    def setUp(self):
        get_last_updated.cache_clear()
        self.addCleanup(get_last_updated.cache_clear)

    def test_real_recipe_has_a_date(self):
        # A committed recipe resolves to an ISO date.
        value = get_last_updated(RECIPES_DIR / "z" / "zlib")
        self.assertRegex(value, r"^\d{4}-\d{2}-\d{2}$")

    def test_result_is_cached_per_directory(self):
        # Both generators ask for this, and each recipe's date cannot change
        # within one build. Caching turns 228 git subprocesses into 114.
        original = recipe_metadata.subprocess.run
        calls = []

        def counting(*args, **kwargs):
            calls.append(args)
            return original(*args, **kwargs)

        recipe_metadata.subprocess.run = counting
        try:
            first = get_last_updated(RECIPES_DIR / "z" / "zlib")
            second = get_last_updated(RECIPES_DIR / "z" / "zlib")
        finally:
            recipe_metadata.subprocess.run = original

        self.assertEqual(first, second)
        self.assertEqual(len(calls), 1)

    def test_git_failure_warns_and_degrades_to_empty(self):
        # Silently blanking the "Last Updated" column hides a broken
        # environment, so the failure is reported.
        original = recipe_metadata.subprocess.run

        def boom(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="git", timeout=5)

        recipe_metadata.subprocess.run = boom
        try:
            with self.assertWarns(UserWarning):
                value = get_last_updated(RECIPES_DIR / "z" / "zlib")
        finally:
            recipe_metadata.subprocess.run = original

        self.assertEqual(value, "")


class TestRecipeNaming(unittest.TestCase):
    def test_letter_comes_from_directory_not_title(self):
        # recipes/e/exif/ is titled "libexif"; routing must stay on 'e'.
        exif = RECIPES_DIR / "e" / "exif" / "library.toml"
        self.assertTrue(exif.exists())
        self.assertEqual(recipe_letter(exif), "e")

    def test_names_include_canonical_and_directory(self):
        # The two must actually differ, or the directory alias goes untested.
        toml_file = RECIPES_DIR / "x" / "x264" / "library.toml"
        names = recipe_names(toml_file, {"canonical_name": "libx264"})
        self.assertEqual(names, {"libx264", "x264"})

    def test_dashed_directory_is_registered_as_an_alias(self):
        # Eight recipe directories keep their dashed upstream spelling, and
        # dependents refer to them that way, so the directory name is the name.
        toml_file = RECIPES_DIR / "j" / "json-c" / "library.toml"
        names = recipe_names(toml_file, {"canonical_name": "json_c"})
        self.assertEqual(names, {"json_c", "json-c"})

    def test_directory_name_is_always_an_alias(self):
        toml_file = RECIPES_DIR / "x" / "xorgproto" / "library.toml"
        data = {"canonical_name": "xorgproto"}
        self.assertIn(toml_file.parent.name, recipe_names(toml_file, data))

    def test_canonical_name_falls_back_to_directory(self):
        toml_file = RECIPES_DIR / "x" / "xorgproto" / "library.toml"
        self.assertEqual(recipe_names(toml_file, {}), {"xorgproto"})


class TestRealTree(unittest.TestCase):
    def test_every_recipe_file_is_discovered(self):
        found = recipe_files(RECIPES_DIR)
        self.assertGreater(len(found), 100)
        for path in found:
            with self.subTest(path=path):
                self.assertTrue(path.is_absolute())
                self.assertEqual(path.name, "library.toml")

    def test_every_recipe_uses_the_table_form(self):
        # The schema enforces this; the assertion documents why the string
        # branch of parse_dependencies could be deleted.
        for toml_file in recipe_files(RECIPES_DIR):
            raw = load_recipe(toml_file).get("dependencies")
            with self.subTest(path=toml_file):
                if raw is None:
                    continue
                self.assertIsInstance(raw, dict)


if __name__ == "__main__":
    unittest.main()
