#!/usr/bin/env python3
"""Tests for verify_recipes.py, the real-build check.

The builds themselves need a network and a toolchain, so they run in CI, not
here. What is pinned here is the logic that decides what gets built and how a
result is judged: dependency order, which recipes a change affects, how a
recipe's linkage is classified, and the link probe's command line.
"""

import tempfile
import unittest
from pathlib import Path

import verify_recipes as vr


def make_recipe(root, name, deps=(), output_type="library", libname=None,
                extra=""):
    d = root / name[0] / name
    d.mkdir(parents=True)
    canonical = name.replace("-", "_")
    lines = [
        f'title = "{name}"', 'version = "1.0"', 'description = "Test."',
        'license = "MIT"', f'canonical_name = "{canonical}"',
        'recipe_url = "https://example.invalid/x.tar.gz"',
        f'sha256 = "{"ab" * 32}"', 'sha256_source = "tofu"',
        f'output_type = "{output_type}"',
    ]
    if libname is not None:
        lines.append(f'libname = "{libname}"')
    lines.append(extra)
    lines.append("[dependencies]")
    lines += [f'{dep} = ""' for dep in deps]
    (d / "library.toml").write_text("\n".join(lines) + "\n")
    (d / "install.sh").write_text("#!/bin/bash\nset -e -o pipefail -u\n")
    return d


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def registry(self):
        return vr.Registry(self.root)


class TestBuildOrder(RegistryTest):
    def test_dependencies_come_first_and_once(self):
        make_recipe(self.root, "zlib")
        make_recipe(self.root, "libpng", ["zlib"])
        make_recipe(self.root, "freetype", ["zlib", "libpng"])
        order = self.registry().build_order(["freetype"])
        self.assertEqual(order, ["zlib", "libpng", "freetype"])

    def test_aliases_resolve_to_one_recipe(self):
        # json-c is the directory, json_c the canonical name.
        make_recipe(self.root, "json-c")
        make_recipe(self.root, "bind", ["json_c"])
        make_recipe(self.root, "cryptsetup", ["json-c"])
        order = self.registry().build_order(["bind", "cryptsetup"])
        self.assertEqual(order, ["json-c", "bind", "cryptsetup"])

    def test_a_cycle_is_reported(self):
        make_recipe(self.root, "aaa", ["bbb"])
        make_recipe(self.root, "bbb", ["aaa"])
        with self.assertRaisesRegex(ValueError, "cycle"):
            self.registry().build_order(["aaa"])


class TestAffectedRecipes(RegistryTest):
    def test_changed_recipe_and_its_dependents(self):
        make_recipe(self.root, "zlib")
        make_recipe(self.root, "libpng", ["zlib"])
        make_recipe(self.root, "freetype", ["libpng"])
        make_recipe(self.root, "unrelated")
        self.assertEqual(
            self.registry().affected({"zlib"}),
            ["zlib", "libpng", "freetype"])

    def test_paths_map_to_recipe_directories(self):
        make_recipe(self.root, "zlib")
        make_recipe(self.root, "json-c")
        names = self.registry().changed_recipes([
            "recipes/z/zlib/install.sh",
            "recipes/j/json-c/library.toml",
            "README.md",
            "recipes/q/removed/install.sh",
        ])
        self.assertEqual(names, {"zlib", "json-c"})


class TestLinkage(RegistryTest):
    def test_classification(self):
        make_recipe(self.root, "zlib")
        make_recipe(self.root, "curl", ["zlib"])
        make_recipe(self.root, "nghttp2")
        providers = {
            "libz.so.1": {"zlib"},
            "libnghttp2.so.14": {"nghttp2"},
            "libcurl.so.4": {"curl"},
        }
        needed = {"libc.so.6", "libz.so.1", "libnghttp2.so.14",
                  "libidn2.so.0", "libcurl.so.4", "libgcc_s.so.1"}
        findings = self.registry().classify_linkage("curl", needed, providers)
        self.assertEqual(findings, [
            "HOST libidn2.so.0",
            "UNDECLARED libnghttp2.so.14 (recipe: nghttp2)",
        ])

    def test_toolchain_libraries_are_exempt(self):
        for soname in ("libc.so.6", "libm.so.6", "ld-linux-x86-64.so.2",
                       "libstdc++.so.6", "libgcc_s.so.1", "libgomp.so.1",
                       "libgfortran.so.5", "libmvec.so.1"):
            with self.subTest(soname=soname):
                self.assertTrue(vr.is_toolchain(soname))
        self.assertFalse(vr.is_toolchain("libz.so.1"))


class TestContractCheck(RegistryTest):
    def test_missing_library_is_reported(self):
        make_recipe(self.root, "zlib", libname="z")
        prefix = self.root / "prefix"
        (prefix / "include").mkdir(parents=True)
        (prefix / "include" / "zlib.h").write_text("")
        (prefix / "lib").mkdir()
        problems = self.registry().contract_problems("zlib", prefix)
        self.assertEqual(len(problems), 1)
        self.assertIn("libz", problems[0])

    def test_complete_library_passes(self):
        make_recipe(self.root, "zlib", libname="z")
        prefix = self.root / "prefix"
        (prefix / "include").mkdir(parents=True)
        (prefix / "include" / "zlib.h").write_text("")
        (prefix / "lib").mkdir()
        (prefix / "lib" / "libz.so").write_text("")
        self.assertEqual(
            self.registry().contract_problems("zlib", prefix), [])

    def test_data_package_needs_files(self):
        make_recipe(self.root, "xcb-proto", output_type="data")
        prefix = self.root / "prefix"
        prefix.mkdir()
        self.assertEqual(
            len(self.registry().contract_problems("xcb-proto", prefix)), 1)
        (prefix / "share").mkdir()
        (prefix / "share" / "xcb.xml").write_text("")
        self.assertEqual(
            self.registry().contract_problems("xcb-proto", prefix), [])


class TestLinkProbe(RegistryTest):
    def test_command_uses_only_library_toml_metadata(self):
        make_recipe(self.root, "cjson", libname="cjson",
                    extra='include_dir = "include/cjson"')
        prefix = Path("/p")
        cmd = self.registry().probe_command("cjson", prefix, Path("/w/probe"))
        self.assertIn("-I/p/include/cjson", cmd)
        self.assertIn("-L/p/lib", cmd)
        self.assertIn("-Wl,-rpath,/p/lib", cmd)
        # --no-as-needed keeps the library even though main() uses nothing,
        # so running the probe proves the dynamic loader can resolve it.
        self.assertLess(cmd.index("-Wl,--no-as-needed"), cmd.index("-lcjson"))

    def test_header_only_and_data_have_no_probe(self):
        make_recipe(self.root, "uthash", extra="header_only = true")
        make_recipe(self.root, "xcb-proto", output_type="data")
        registry = self.registry()
        self.assertIsNone(registry.probe_command("uthash", Path("/p"),
                                                 Path("/w/probe")))
        self.assertIsNone(registry.probe_command("xcb-proto", Path("/p"),
                                                 Path("/w/probe")))


class TestRealRegistry(unittest.TestCase):
    def test_the_real_tree_has_a_build_order(self):
        registry = vr.Registry()
        order = registry.build_order(registry.names())
        self.assertEqual(len(order), len(registry.names()))


if __name__ == "__main__":
    unittest.main()
