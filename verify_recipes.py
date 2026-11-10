#!/usr/bin/env python3
"""Build recipes for real and check what they install.

Usage:
  verify_recipes.py [--root DIR] [--force] NAME...
  verify_recipes.py [--root DIR] [--force] --all
  verify_recipes.py [--root DIR] [--force] --changed-since GIT-REF

Each recipe's published install.sh is rendered and run with COFFEE_HOME set to
<root>/coffee, after its registry dependencies, which are exposed to the build
the way coffee exposes them: PKG_CONFIG_PATH, CMAKE_PREFIX_PATH, CPPFLAGS,
LDFLAGS, PATH and LD_LIBRARY_PATH. The installed prefix must then pass:

- the contract: include_dir non-empty and lib<libname>.so or .a for each
  libname; bin/ for executables; some files for data packages
- the linkage audit: every shared library an installed ELF file needs directly
  (DT_NEEDED) comes from the recipe itself, a declared dependency, or the
  toolchain. UNDECLARED means another recipe provides it but it is not in the
  dependency closure; HOST means no recipe provides it.
- the link probe: an empty program linked with -l<libname> for every libname,
  using only library.toml's include_dir and lib_dir, must build and run.

--changed-since builds the recipes changed since a git ref plus everything
that depends on them. Exit status is non-zero if any recipe fails.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

from recipe_metadata import (
    RECIPES_DIR,
    REPO_ROOT,
    load_recipe,
    recipe_dependencies,
    recipe_files,
    recipe_names,
    recipe_usage,
)
from recipe_script import render_install_script

DEFAULT_ROOT = REPO_ROOT / "verify"

# Runtime libraries of the compiler and the C library: never from a recipe.
TOOLCHAIN = re.compile(
    r"^(?:libc|libm|libdl|libpthread|librt|libresolv|libutil|libanl|libmvec"
    r"|ld-linux[\w.-]*|libgcc_s|libstdc\+\+|libgomp|libatomic|libgfortran"
    r"|libquadmath)\.so")

PROBE_SOURCE = "int main(void) { return 0; }\n"


def is_toolchain(soname: str) -> bool:
    return bool(TOOLCHAIN.match(soname))


class Registry:
    """The recipe tree, indexed by directory name with aliases resolved."""

    def __init__(self, base_dir: Path = RECIPES_DIR):
        self.recipes = {}
        self.alias = {}
        for toml_file in recipe_files(base_dir):
            data = load_recipe(toml_file)
            name = toml_file.parent.name
            self.recipes[name] = (toml_file, data)
            for alias in recipe_names(toml_file, data):
                self.alias[alias] = name

    def names(self) -> list[str]:
        return sorted(self.recipes)

    def data(self, name: str) -> dict:
        return self.recipes[name][1]

    def deps(self, name: str) -> list[str]:
        toml_file, data = self.recipes[name]
        return [self.alias[d] for d in recipe_dependencies(toml_file, data)]

    def build_order(self, names) -> list[str]:
        """Return names and their dependencies, dependencies first."""
        order, done, active = [], set(), []

        def visit(name):
            if name in done:
                return
            if name in active:
                raise ValueError(f"dependency cycle: "
                                 f"{' -> '.join(active + [name])}")
            active.append(name)
            for dep in self.deps(name):
                visit(dep)
            active.pop()
            done.add(name)
            order.append(name)

        for name in names:
            visit(self.alias[name])
        return order

    def closure(self, name: str) -> list[str]:
        """Return the dependencies of name, without name itself."""
        return self.build_order([name])[:-1]

    def affected(self, changed) -> list[str]:
        """Return changed recipes and all their dependents, in build order."""
        affected = set(changed)
        for name in self.names():
            if affected & set(self.closure(name)):
                affected.add(name)
        return [n for n in self.build_order(sorted(affected)) if n in affected]

    def changed_recipes(self, paths) -> set[str]:
        """Return the existing recipes that a list of repo paths touches."""
        names = set()
        for path in paths:
            parts = Path(path).parts
            if len(parts) >= 3 and parts[0] == "recipes" and \
                    parts[2] in self.recipes:
                names.add(parts[2])
        return names

    def prefix(self, root: Path, name: str) -> Path:
        data = self.data(name)
        return root / "coffee" / data["canonical_name"] / data["version"]

    def contract_problems(self, name: str, prefix: Path) -> list[str]:
        data = self.data(name)
        usage = recipe_usage(data)
        output_type = data["output_type"]
        problems = []
        if output_type in ("library", "both"):
            include = prefix / usage["include_dir"]
            if not include.is_dir() or not any(include.iterdir()):
                problems.append(f"empty or missing {include}")
            lib = prefix / usage["lib_dir"]
            for libname in usage["libname"]:
                if not any((lib / f"lib{libname}{ext}").exists()
                           for ext in (".so", ".a")):
                    problems.append(f"no lib{libname}.so or .a in {lib}")
        if output_type in ("executable", "both"):
            bin_dir = prefix / "bin"
            if not bin_dir.is_dir() or not any(bin_dir.iterdir()):
                problems.append(f"empty or missing {bin_dir}")
        if output_type == "data" and not (
                prefix.is_dir() and any(p.is_file() for p in prefix.rglob("*"))):
            problems.append(f"nothing installed under {prefix}")
        return problems

    def classify_linkage(self, name: str, needed, providers) -> list[str]:
        """Return UNDECLARED/HOST findings for a recipe's DT_NEEDED sonames.

        providers maps a soname to the recipes whose prefixes contain it.
        """
        allowed = {name, *self.closure(name)}
        findings = []
        for soname in needed:
            if is_toolchain(soname):
                continue
            owners = providers.get(soname, set())
            if owners & allowed:
                continue
            if owners:
                findings.append(f"UNDECLARED {soname} (recipe: "
                                f"{', '.join(sorted(owners))})")
            else:
                findings.append(f"HOST {soname}")
        return sorted(findings)

    def probe_command(self, name: str, prefix: Path, output: Path):
        """Return the link probe's cc command, or None if nothing links."""
        usage = recipe_usage(self.data(name))
        if usage["header_only"] or not usage["libname"]:
            return None
        lib = prefix / usage["lib_dir"]
        return ["cc", "-x", "c", "-", "-o", str(output),
                f"-I{prefix / usage['include_dir']}", f"-L{lib}",
                f"-Wl,-rpath,{lib}", "-Wl,--no-as-needed",
                *(f"-l{libname}" for libname in usage["libname"])]


def needed_sonames(prefix: Path) -> set[str]:
    """Return the DT_NEEDED entries of every ELF file under prefix."""
    sonames = set()
    for path in prefix.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        with open(path, "rb") as f:
            if f.read(4) != b"\x7fELF":
                continue
        out = subprocess.run(["readelf", "-d", str(path)],
                             capture_output=True, text=True).stdout
        sonames.update(re.findall(r"\(NEEDED\).*\[(.+?)\]", out))
    return sonames


def soname_providers(registry: Registry, root: Path) -> dict[str, set[str]]:
    """Map each shared-library file name under root to the recipes owning it."""
    by_prefix = {registry.prefix(root, n): n for n in registry.names()}
    providers = {}
    for prefix, name in by_prefix.items():
        if prefix.is_dir():
            for lib in prefix.rglob("*.so*"):
                providers.setdefault(lib.name, set()).add(name)
    return providers


def build_env(registry: Registry, root: Path, deps) -> dict:
    """Return the environment coffee would give a build with these deps."""
    pc, cmake, cpp, ld, rpath, path = [], [], [], [], [], []
    for dep in deps:
        prefix = registry.prefix(root, dep)
        usage = recipe_usage(registry.data(dep))
        cmake.append(str(prefix))
        for libdir in dict.fromkeys(("lib", usage["lib_dir"])):
            pc.append(str(prefix / libdir / "pkgconfig"))
            ld.append(f"-L{prefix / libdir}")
            rpath.append(str(prefix / libdir))
        pc.append(str(prefix / "share" / "pkgconfig"))
        for include in dict.fromkeys(("include", usage["include_dir"])):
            cpp.append(f"-I{prefix / include}")
        path.append(str(prefix / "bin"))
    return {
        **os.environ,
        "COFFEE_HOME": str(root / "coffee"),
        "TMPDIR": str(root / "tmp"),
        "PKG_CONFIG_PATH": os.pathsep.join(pc),
        "CMAKE_PREFIX_PATH": os.pathsep.join(cmake),
        "CPPFLAGS": " ".join(cpp),
        "LDFLAGS": " ".join(ld + [f"-Wl,-rpath,{p}" for p in rpath]),
        "LD_LIBRARY_PATH": os.pathsep.join(rpath),
        "PATH": os.pathsep.join(path + [os.environ.get("PATH", "")]),
    }


class Verifier:
    def __init__(self, registry: Registry, root: Path, force=False):
        self.registry = registry
        self.root = root
        self.force = force
        self.status = {}
        for sub in ("coffee", "logs", "tmp", "scripts", "ok"):
            (root / sub).mkdir(parents=True, exist_ok=True)

    def verify(self, name: str) -> list[str]:
        """Build one recipe (dependencies already built); return problems."""
        if name in self.status:
            return self.status[name]
        failed = [d for d in self.registry.closure(name) if self.status.get(d)]
        if failed:
            return self._record(name, [f"dependency {failed[0]} failed"])
        marker = self.root / "ok" / name
        if marker.exists() and not self.force:
            return self._record(name, [])
        marker.unlink(missing_ok=True)

        toml_file, data = self.registry.recipes[name]
        script = self.root / "scripts" / f"{name}.sh"
        script.write_text(render_install_script(
            (toml_file.parent / "install.sh").read_text(), data))
        prefix = self.registry.prefix(self.root, name)
        log = self.root / "logs" / f"{name}.log"
        deps = self.registry.closure(name)
        with open(log, "w") as out:
            result = subprocess.run(
                ["bash", str(script)], stdout=out, stderr=subprocess.STDOUT,
                env=build_env(self.registry, self.root, deps),
                cwd=self.root / "tmp")
        if result.returncode != 0:
            return self._record(name, [f"exit {result.returncode}, see {log}"])

        problems = self.registry.contract_problems(name, prefix)
        problems += self.registry.classify_linkage(
            name, needed_sonames(prefix),
            soname_providers(self.registry, self.root))
        problems += self.probe(name, prefix)
        if not problems:
            marker.write_text("")
        return self._record(name, problems)

    def probe(self, name: str, prefix: Path) -> list[str]:
        output = self.root / "tmp" / f"probe-{name}"
        command = self.registry.probe_command(name, prefix, output)
        if command is None:
            return []
        built = subprocess.run(command, input=PROBE_SOURCE,
                               capture_output=True, text=True)
        if built.returncode != 0:
            return [f"link probe failed: {built.stderr.strip()[:300]}"]
        ran = subprocess.run([str(output)], capture_output=True, text=True)
        output.unlink(missing_ok=True)
        if ran.returncode != 0:
            return [f"link probe does not run: {ran.stderr.strip()[:300]}"]
        return []

    def _record(self, name, problems):
        self.status[name] = problems
        label = "OK  " if not problems else "FAIL"
        print(f"{label} {name}", flush=True)
        for problem in problems:
            print(f"     {problem}", flush=True)
        return problems


def git_changed_paths(ref: str) -> list[str]:
    out = subprocess.run(["git", "diff", "--name-only", f"{ref}...HEAD"],
                         capture_output=True, text=True, check=True,
                         cwd=REPO_ROOT).stdout
    return out.split()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("names", nargs="*")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--force", action="store_true",
                        help="rebuild the named recipes even if they passed")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true")
    group.add_argument("--changed-since", metavar="REF")
    args = parser.parse_args(argv)

    registry = Registry()
    if args.all:
        targets = registry.names()
    elif args.changed_since:
        targets = registry.affected(
            registry.changed_recipes(git_changed_paths(args.changed_since)))
    else:
        targets = [registry.alias[n] for n in args.names]
    if not targets:
        print("nothing to verify")
        return 0

    verifier = Verifier(registry, args.root.resolve())
    for name in registry.build_order(targets):
        verifier.force = args.force and name in targets
        verifier.verify(name)

    failed = sorted(n for n in targets if verifier.status.get(n))
    print(f"\n{len(targets) - len(failed)} of {len(targets)} verified")
    if failed:
        print("failed: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
