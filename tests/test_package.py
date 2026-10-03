"""Offline distribution and installation contracts; never use live home folders."""

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
NAME = "handdrawn-scientific-figures"


def load_script(name):
    path = REPO / "scripts" / (name + ".py")
    assert path.is_file(), f"Required distribution utility missing: {path.name}"
    spec = importlib.util.spec_from_file_location("hdsf_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(root):
    skill = root / "skills" / NAME
    (skill / "references").mkdir(parents=True)
    (skill / "assets").mkdir()
    (skill / "scripts").mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: " + NAME + "\ndescription: Draw reproducible figures offline.\n---\n"
        "Read [guide](references/guide.md). See ![sample](assets/example.svg).\n"
        "Use [renderer](scripts/render.py).\n",
        encoding="utf-8",
    )
    (skill / "references" / "guide.md").write_text("Guide.\n", encoding="utf-8")
    (skill / "assets" / "example.svg").write_text("<svg/>\n", encoding="utf-8")
    (skill / "scripts" / "render.py").write_text("print('offline')\n", encoding="utf-8")
    (root / "README.md").write_text("Public distribution\n", encoding="utf-8")
    return skill


def digest(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file()
    }


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.skill = fixture(self.repo)
        self.home = self.root / "home"

    def test_valid_self_contained_skill(self):
        self.assertEqual(load_script("validate").validate_skill(self.skill), [])

    def test_https_links_are_not_windows_absolute_paths(self):
        (self.skill / "references" / "guide.md").write_text(
            "Read [official docs](https://example.com/docs).\n", encoding="utf-8"
        )
        self.assertEqual(load_script("validate").validate_skill(self.skill), [])

    def test_windows_absolute_paths_remain_rejected(self):
        for local_path in [r"C:\Users\alvin\private\font.ttf", "D:/figures/result.svg"]:
            with self.subTest(path=local_path):
                (self.skill / "references" / "guide.md").write_text(
                    "Local path: `" + local_path + "`.\n", encoding="utf-8"
                )
                self.assertTrue(
                    any(
                        "absolute path" in e.lower()
                        for e in load_script("validate").validate_skill(self.skill)
                    )
                )

    def test_missing_link_and_frontmatter_are_reported(self):
        (self.skill / "assets" / "example.svg").unlink()
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text().replace("description:", "wrong:"))
        errors = load_script("validate").validate_skill(self.skill)
        self.assertTrue(any("description" in e for e in errors))
        self.assertTrue(any("example.svg" in e for e in errors))

    def test_unfinished_scaffold_and_escaping_links_fail(self):
        with (self.skill / "references" / "guide.md").open("a") as f:
            f.write("\nTODO: write this\n[external local](../../README.md)\n")
        errors = load_script("validate").validate_skill(self.skill)
        self.assertTrue(any("unfinished" in e.lower() for e in errors))
        self.assertTrue(any("outside" in e.lower() for e in errors))

    def test_standalone_scaffold_marker_is_rejected(self):
        (self.skill / "references" / "guide.md").write_text("TODO\n")
        self.assertTrue(
            any(
                "unfinished" in e.lower()
                for e in load_script("validate").validate_skill(self.skill)
            )
        )

    def test_style_font_files_must_exist_inside_assets(self):
        (self.skill / "assets" / "style.json").write_text(
            json.dumps(
                {
                    "name": NAME,
                    "fonts": {
                        "title": {"file": "fonts/missing.ttf", "family": "Title"},
                        "body": {"file": "../../README.md", "family": "Body"},
                    },
                }
            )
        )
        errors = load_script("validate").validate_skill(self.skill)
        self.assertTrue(any("missing.ttf" in e for e in errors))
        self.assertTrue(any("font" in e.lower() and "outside" in e.lower() for e in errors))

    def test_backticked_bundled_paths_resolve_from_skill_root(self):
        (self.skill / "references" / "guide.md").write_text("Use `scripts/render.py`.\n")
        self.assertEqual(load_script("validate").validate_skill(self.skill), [])

    def test_existing_archive_is_never_overwritten(self):
        output = self.root / "keep.zip"
        output.write_bytes(b"existing user bytes")
        with self.assertRaises(FileExistsError):
            load_script("package").build_archive(self.repo, output)
        self.assertEqual(output.read_bytes(), b"existing user bytes")

    def test_empty_frontmatter_literal_description_is_rejected(self):
        p = self.skill / "SKILL.md"
        p.write_text(
            p.read_text().replace(
                "description: Draw reproducible figures offline.", "description: |"
            )
        )
        errors = load_script("validate").validate_skill(self.skill)
        self.assertTrue(any("description" in e for e in errors))

    def test_default_install_is_dry_run(self):
        targets = load_script("install").install_skill(self.skill, "both", home=self.home)
        self.assertEqual(
            targets,
            [self.home / ".agents" / "skills" / NAME, self.home / ".claude" / "skills" / NAME],
        )
        self.assertFalse(self.home.exists())

    def test_apply_copies_complete_skill_without_mutating_source(self):
        before = digest(self.skill)
        targets = load_script("install").install_skill(
            self.skill, "both", home=self.home, apply=True
        )
        self.assertEqual(digest(self.skill), before)
        for target in targets:
            self.assertEqual(digest(target), before)

    def test_project_scope_stays_in_explicit_project(self):
        project = self.root / "project"
        project.mkdir()
        targets = load_script("install").install_skill(
            self.skill, "codex", scope="project", project_root=project, apply=True
        )
        self.assertEqual(targets, [project / ".agents" / "skills" / NAME])
        self.assertFalse(self.home.exists())

    def test_collision_preflight_never_touches_other_destination(self):
        existing = self.home / ".claude" / "skills" / NAME
        existing.mkdir(parents=True)
        (existing / "mine.txt").write_text("keep")
        with self.assertRaises(FileExistsError):
            load_script("install").install_skill(self.skill, "both", home=self.home, apply=True)
        self.assertEqual((existing / "mine.txt").read_text(), "keep")
        self.assertFalse((self.home / ".agents").exists())

    def test_copy_failure_rolls_back_only_owned_directories(self):
        installer = load_script("install")
        shared = self.home / ".agents" / "skills"
        shared.mkdir(parents=True)
        (shared / "existing.txt").write_text("keep")
        original = installer.shutil.copytree

        def failing_copy(source, target, *args, **kwargs):
            if Path(target) == self.home / ".claude" / "skills" / NAME:
                (Path(target) / "partial.txt").write_text("partial")
                raise OSError("injected copy failure")
            return original(source, target, *args, **kwargs)

        with patch.object(installer.shutil, "copytree", side_effect=failing_copy):
            with self.assertRaisesRegex(OSError, "injected"):
                installer.install_skill(self.skill, "both", home=self.home, apply=True)
        self.assertEqual((shared / "existing.txt").read_text(), "keep")
        self.assertFalse((shared / NAME).exists())
        self.assertFalse((self.home / ".claude").exists())

    def test_source_symlink_is_rejected(self):
        link = self.skill / "assets" / "linked.svg"
        try:
            link.symlink_to(self.skill / "assets" / "example.svg")
        except OSError:
            self.skipTest("Symlink privilege unavailable")
        with self.assertRaisesRegex(ValueError, "[Ss]ymlink"):
            load_script("install").install_skill(self.skill, "codex", home=self.home, apply=True)
        self.assertFalse(self.home.exists())

    def test_destination_symlink_cannot_escape_selected_root(self):
        self.home.mkdir()
        outside = self.root / "outside"
        outside.mkdir()
        try:
            (self.home / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink privilege unavailable")
        with self.assertRaisesRegex(ValueError, "outside|[Ss]ymlink"):
            load_script("install").install_skill(self.skill, "codex", home=self.home, apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_public_archive_has_one_root_and_excludes_private_outputs(self):
        for rel in [
            ".git/config",
            "private/secret.txt",
            "examples/__pycache__/x.pyc",
            "evaluations/raw/screenshots/capture.png",
            "examples/old.zip",
        ]:
            p = self.repo / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("exclude")
        output = self.root / "public.zip"
        load_script("package").build_archive(self.repo, output)
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
        self.assertTrue(all(p.startswith(NAME + "/") for p in names))
        self.assertIn(NAME + "/README.md", names)
        self.assertFalse(
            any("secret" in p or "capture" in p or ".pyc" in p or "old.zip" in p for p in names)
        )

    def test_skill_archive_unzips_and_validates_in_isolation(self):
        output = self.root / "skill.zip"
        load_script("package").build_archive(self.repo, output, skill_only=True)
        extraction = self.root / "isolated"
        with zipfile.ZipFile(output) as archive:
            archive.extractall(extraction)
        self.assertEqual(digest(extraction / NAME), digest(self.skill))
        self.assertEqual(load_script("validate").validate_skill(extraction / NAME), [])

    def test_archive_rejects_absolute_local_example_paths(self):
        (self.repo / "examples").mkdir()
        (self.repo / "examples" / "sample.py").write_text(
            'path = "/Users/example-user/private/data"\n'
        )
        with self.assertRaisesRegex(ValueError, "absolute|local path"):
            load_script("package").build_archive(self.repo, self.root / "invalid.zip")
        self.assertFalse((self.root / "invalid.zip").exists())

    def test_archive_rejects_machine_temp_paths_in_examples(self):
        (self.repo / "examples").mkdir()
        (self.repo / "examples" / "sample.json").write_text(
            '{"output": "/var/folders/private/result.svg"}'
        )
        with self.assertRaisesRegex(ValueError, "absolute|local path"):
            load_script("package").build_archive(self.repo, self.root / "invalid.zip")

    def test_public_zip_utilities_work_without_checkout_imports(self):
        for name in ["package", "install", "validate"]:
            source = REPO / "scripts" / (name + ".py")
            self.assertTrue(
                source.is_file(), f"Required distribution utility missing: {source.name}"
            )
            destination = self.repo / "scripts" / source.name
            destination.parent.mkdir(exist_ok=True)
            destination.write_bytes(source.read_bytes())
        output = self.root / "public.zip"
        load_script("package").build_archive(self.repo, output)
        extraction = self.root / "isolated"
        with zipfile.ZipFile(output) as archive:
            archive.extractall(extraction)
        isolated = extraction / NAME
        for command in [
            ["scripts/validate.py"],
            ["scripts/install.py", "--home", str(self.home)],
            ["scripts/package.py", "--skill-only", "--output", str(self.root / "repack.zip")],
        ]:
            run = subprocess.run(
                [sys.executable] + command, cwd=isolated, capture_output=True, text=True
            )
            self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
