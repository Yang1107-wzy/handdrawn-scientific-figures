#!/usr/bin/env python3
"""Create a clean public repository ZIP, or a standalone skill ZIP, entirely offline."""

import argparse
import importlib.util
import os
import sys
import tempfile
import zipfile
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "hdsf_validation", Path(__file__).with_name("validate.py")
)
_validation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validation)
NAME = _validation.NAME
PUBLIC_DIRS = {"skills", "examples", "docs", "scripts", "tests", ".github", "evaluations"}
PUBLIC_FILES = {
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "requirements.txt",
    "pyproject.toml",
    ".gitignore",
    "SOURCES.md",
    "DIST_REPORT.md",
}
EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "build",
    "dist",
    "tmp",
    "temp",
    "outputs",
    "private",
    "raw",
    "screenshots",
    "build_workspace",
}
ARCHIVE_SUFFIXES = (".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar", ".whl")
TEXT_SUFFIXES = {".py", ".json", ".jsonl", ".md", ".txt", ".yaml", ".yml", ".toml", ".csv", ".svg"}


def _excluded(relative):
    parts = [p.lower() for p in relative.parts]
    return (
        any(p in EXCLUDED_PARTS or "screenshot" in p for p in parts)
        or relative.name.lower().endswith(ARCHIVE_SUFFIXES)
        or relative.suffix.lower() in {".pyc", ".pyo", ".tmp", ".log"}
        or relative.name in {".DS_Store", "BUILD_WORKSPACE.txt"}
    )


def build_archive(repo, output, skill_only=False):
    repo = Path(repo).resolve()
    output = Path(output).absolute()
    skill = repo / "skills" / NAME
    errors = _validation.validate_skill(skill)
    if errors:
        raise ValueError("Invalid skill: " + "; ".join(errors))
    source = skill if skill_only else repo
    files = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if _excluded(relative):
            continue
        if not skill_only and not (
            relative.parts[0] in PUBLIC_DIRS or relative.as_posix() in PUBLIC_FILES
        ):
            continue
        if path.is_symlink():
            raise ValueError(f"Source symlink is not allowed: {relative}")
        if not path.is_file() or path.absolute() == output:
            continue
        if (
            not skill_only and relative.parts[0] == "examples"
        ) or relative.as_posix() == "DIST_REPORT.md":
            if path.suffix.lower() in TEXT_SUFFIXES and _validation.LOCAL_PATH.search(
                path.read_text(encoding="utf-8")
            ):
                raise ValueError(f"Local absolute path is not public: {relative}")
        files.append((path, relative))
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Archive already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".hdsf-package-", suffix=".tmp", dir=output.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path, relative in files:
                item = zipfile.ZipInfo(
                    f"{NAME}/{relative.as_posix()}", date_time=(2020, 1, 1, 0, 0, 0)
                )
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                archive.writestr(item, path.read_bytes())
        # Exclusive final creation prevents overwriting a concurrently created archive.
        with output.open("xb") as destination, open(temporary, "rb") as source_file:
            import shutil

            shutil.copyfileobj(source_file, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--skill-only", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        output = build_archive(args.repo_root, args.output, args.skill_only)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Created {'standalone skill' if args.skill_only else 'public repository'} ZIP: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
