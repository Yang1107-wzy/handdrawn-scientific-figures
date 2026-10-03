#!/usr/bin/env python3
"""Copy the complete skill to Codex and/or Claude; dry-run unless --apply is set."""

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "hdsf_validation", Path(__file__).with_name("validate.py")
)
_validation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validation)
NAME = _validation.NAME


def install_skill(
    source, client="codex", *, home=None, scope="user", project_root=None, apply=False
):
    source = Path(source)
    if _validation.source_symlinks(source):
        raise ValueError("Source symlink is not allowed")
    errors = _validation.validate_skill(source)
    if errors:
        raise ValueError("Invalid skill: " + "; ".join(errors))
    if client not in ("codex", "claude", "both"):
        raise ValueError("client must be codex, claude, or both")
    if scope not in ("user", "project"):
        raise ValueError("scope must be user or project")
    if scope == "project":
        if project_root is None:
            raise ValueError("project scope requires --project-root")
        root = Path(project_root).expanduser().absolute()
        if not root.is_dir():
            raise ValueError("project root must be an existing directory")
    else:
        root = Path(home).expanduser().absolute() if home is not None else Path.home()
    clients = ("codex", "claude") if client == "both" else (client,)
    targets = [
        root / (".agents" if name == "codex" else ".claude") / "skills" / NAME for name in clients
    ]
    for target in targets:
        if not target.resolve().is_relative_to(root.resolve()):
            raise ValueError("Destination resolves outside selected root")
        for ancestor in [target, *target.parents]:
            if ancestor == root:
                break
            if ancestor.is_symlink():
                raise ValueError("Destination symlink is not allowed")
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Destination already exists: {target}")
        if source.resolve().is_relative_to(target.resolve()) or target.resolve().is_relative_to(
            source.resolve()
        ):
            raise ValueError("Source and destination must not contain one another")
    if not apply:
        return targets
    owned_parents = []
    owned_targets = []
    try:
        for target in targets:
            missing = []
            ancestor = target.parent
            while not ancestor.exists():
                missing.append(ancestor)
                ancestor = ancestor.parent
            for directory in reversed(missing):
                directory.mkdir()  # Never claim a pre-existing directory as ours.
                owned_parents.append(directory)
            target.mkdir()
            owned_targets.append(target)
            shutil.copytree(source, target, dirs_exist_ok=True)
    except BaseException:
        for target in reversed(owned_targets):
            shutil.rmtree(target)
        for directory in reversed(owned_parents):
            try:
                directory.rmdir()  # Preserve anything concurrently created by another call.
            except OSError:
                pass
        raise
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=Path(__file__).resolve().parents[1] / "skills" / NAME
    )
    parser.add_argument("--client", choices=("codex", "claude", "both"), default="codex")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--home", type=Path, help="Override home for portable tests")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument(
        "--apply", action="store_true", help="Copy files; existing destinations always fail"
    )
    args = parser.parse_args(argv)
    try:
        targets = install_skill(
            args.source,
            args.client,
            home=args.home,
            scope=args.scope,
            project_root=args.project_root,
            apply=args.apply,
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for target in targets:
        print(f"{'Installed' if args.apply else 'Dry run; would install'}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
