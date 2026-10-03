#!/usr/bin/env python3
"""Validate a portable skill without loading tools, APIs, or rendering dependencies."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

NAME = "handdrawn-scientific-figures"
LOCAL_PATH = re.compile(
    r"/Users/|/home/[^/\s]+/|/var/folders/|/private/tmp/|/tmp/|/Volumes/|\b[A-Za-z]:[\\/]|file://"
)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
UNFINISHED = re.compile(
    r"\b(?:TODO|FIXME|TBD)\s*:|\[(?:TODO|TBD|INSERT)[^\]]*\]|<(?:TODO|TBD)[^>]*>"
    r"|^\s*(?:[-*]\s+)?(?:TODO|FIXME|TBD)\s*$",
    re.MULTILINE,
)


def source_symlinks(root):
    """Find links before following any source content."""
    root = Path(root)
    if root.is_symlink():
        return [root]
    return [p for p in root.rglob("*") if p.is_symlink()]


def validate_skill(root):
    root = Path(root)
    errors = []
    links = source_symlinks(root)
    if links:
        return [f"Source symlink is not portable: {p.name}" for p in links]
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return ["Missing SKILL.md"]
    content = skill_file.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", content, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md requires simple YAML frontmatter")
    else:
        fields = dict(re.findall(r"^([A-Za-z][\w-]*):\s*([^\n]*)", frontmatter[1], re.MULTILINE))
        # Minimal YAML block-scalar support keeps this utility dependency free.
        for field, value in list(fields.items()):
            if value.strip() in ("|", ">", "|-", ">-", "|+", ">+"):
                block = re.search(
                    r"^" + re.escape(field) + r":[^\n]*\n((?:[ \t]+[^\n]*(?:\n|$))*)",
                    frontmatter[1] + "\n",
                    re.MULTILINE,
                )
                fields[field] = block[1].strip() if block else ""
        for field in ("name", "description"):
            if not fields.get(field, "").strip().strip("\"'"):
                errors.append(f"Missing nonempty frontmatter {field}")
        name = fields.get("name", "").strip().strip("\"'")
        if name != NAME:
            errors.append(f"Frontmatter name must be {NAME}")
    resolved_root = root.resolve()
    style_file = root / "assets" / "style.json"
    if style_file.is_file():
        try:
            style = json.loads(style_file.read_text(encoding="utf-8"))
            if style.get("name") != NAME:
                errors.append(f"Style name must match {NAME}")
            fonts = style.get("fonts")
            if not isinstance(fonts, dict) or not fonts:
                errors.append("Style requires bundled font definitions")
            else:
                for role, font in fonts.items():
                    if not isinstance(font, dict) or not isinstance(font.get("file"), str):
                        errors.append(f"Style font {role} requires a file")
                        continue
                    font_path = (style_file.parent / font["file"]).resolve()
                    if not font_path.is_relative_to(style_file.parent.resolve()):
                        errors.append(f"Style font outside assets: {font['file']}")
                    elif not font_path.is_file() or font_path.stat().st_size == 0:
                        errors.append(f"Missing or empty style font: {font['file']}")
        except (ValueError, TypeError, AttributeError) as exc:
            errors.append(f"Invalid assets/style.json: {exc}")
    for markdown in sorted(root.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        label = markdown.relative_to(root).as_posix()
        if UNFINISHED.search(text):
            errors.append(f"Unfinished scaffold in {label}")
        if LOCAL_PATH.search(text):
            errors.append(f"Local absolute path in {label}")
        targets = [
            (raw, markdown.parent) for raw in LINK.findall(text) + REFERENCE_LINK.findall(text)
        ]
        # Backticked paths are common in skill prose. Check concrete bundled paths.
        targets += [
            (raw, root)
            for raw in re.findall(r"`((?:references|assets|scripts)/[^`\s*{}<>]+)`", text)
        ]
        for raw, base in targets:
            target = raw.strip().split(' "', 1)[0].strip("<>")
            parts = urlsplit(target)
            if parts.scheme in ("http", "https", "mailto") or not parts.path:
                continue
            if parts.scheme or Path(unquote(parts.path)).is_absolute():
                errors.append(f"Unsupported absolute resource in {label}: {target}")
                continue
            path = (base / unquote(parts.path)).resolve()
            if not path.is_relative_to(resolved_root):
                errors.append(f"Resource outside skill in {label}: {target}")
            elif not path.exists():
                errors.append(f"Missing resource in {label}: {target}")
    return sorted(set(errors))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", type=Path, default=Path(__file__).resolve().parents[1] / "skills" / NAME
    )
    args = parser.parse_args(argv)
    try:
        errors = validate_skill(args.path)
    except (OSError, UnicodeError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {NAME}: portable local resources and frontmatter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
