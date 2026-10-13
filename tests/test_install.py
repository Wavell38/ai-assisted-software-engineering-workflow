"""Installer acceptance tests; every destination is below a temporary directory."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workflow_install", REPO / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow tests é ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.home = self.base / "user home"
        self.codex = self.base / "custom codex"
        self.skills = self.home / ".agents/skills"
        self.doc = self.skills / installer.SKILLS[0]
        self.review = self.skills / installer.SKILLS[1]
        self.instructions = self.codex / "AGENTS.md"
        # Copy only distributable sources, never local Codex state or the Git database.
        paths = ["VERSION", "agents/GLOBAL_AGENTS_SECTION.md", "scripts/install.py", *installer.GUIDES, *installer.TEMPLATES]
        paths += [f"review/{name}/SKILL.md" for name in installer.SKILLS]
        paths += [f"review/{installer.SKILLS[1]}/{role}-reviewer.toml" for role in installer.REVIEWERS]
        for name in paths:
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, target)

    def run_install(self, check=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.install(self.source, self.home, self.codex, check=check)

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def snapshot(self):
        return {str(p.relative_to(self.base)): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.base.rglob("*") if p.is_file()}

    def test_first_install_and_complete_resources(self):
        self.assertTrue(self.run_install())
        for relative in installer.GUIDES:
            self.assertEqual((self.doc / "references" / relative).read_bytes(), (self.source / relative).read_bytes())
        for relative in installer.TEMPLATES:
            self.assertEqual((self.doc / "assets" / relative).read_bytes(), (self.source / relative).read_bytes())
        for role in installer.REVIEWERS:
            name = f"{role}-reviewer.toml"
            source = self.source / "review/review-and-remediate" / name
            self.assertEqual((self.codex / "agents" / name).read_bytes(), source.read_bytes())
            self.assertEqual((self.review / name).read_bytes(), source.read_bytes())
            profile = tomllib.loads(source.read_text(encoding="utf-8"))
            self.assertEqual(profile["name"], f"{role}_reviewer")
            self.assertEqual(profile["model"], "gpt-6.1-sol")
            self.assertEqual(profile["model_reasoning_effort"], "xhigh" if role == "architecture" else "high")
        for root in (self.doc, self.review):
            self.assertEqual((root / "VERSION").read_bytes(), (self.source / "VERSION").read_bytes())
        expected = (self.source / "agents/GLOBAL_AGENTS_SECTION.md").read_bytes().strip() + b"\n"
        self.assertEqual(self.instructions.read_bytes(), expected)
        self.assertTrue(self.run_install(check=True))

    def test_second_install_does_not_change_files_or_mtimes(self):
        self.run_install()
        before = self.snapshot()
        self.run_install()
        self.assertEqual(self.snapshot(), before)

    def test_source_update_and_personal_files(self):
        self.run_install()
        source = self.source / installer.GUIDES[0]
        source.write_bytes(source.read_bytes() + b"\nNew policy.\n")
        self.write(self.doc / "personal.txt", b"notes")
        self.write(self.codex / "agents/personal.toml", b"personal configuration")
        self.write(self.codex / "config.toml", b"personal settings")
        self.run_install()
        self.assertEqual((self.doc / "references" / installer.GUIDES[0]).read_bytes(), source.read_bytes())
        self.assertEqual((self.doc / "personal.txt").read_bytes(), b"notes")
        self.assertEqual((self.codex / "agents/personal.toml").read_bytes(), b"personal configuration")
        self.assertEqual((self.codex / "config.toml").read_bytes(), b"personal settings")

    def test_legacy_takeover_backed_up_and_extra_files_preserved(self):
        self.write(self.doc / "SKILL.md", b"legacy skill")
        self.write(self.doc / "personal.txt", b"personal")
        self.write(self.codex / "agents/tests-reviewer.toml", b"legacy reviewer")
        self.write(self.instructions, b"My rules\r\n")
        self.run_install()
        backup_contents = [p.read_bytes() for p in self.base.rglob("*") if p.is_file() and ".workflow-ia-backups" in p.parts]
        for old in (b"legacy skill", b"legacy reviewer", b"My rules\r\n"):
            self.assertIn(old, backup_contents)
        self.assertEqual((self.doc / "personal.txt").read_bytes(), b"personal")
        self.assertFalse(any(".workflow-ia-backups" in p.parts for p in self.skills.rglob("*")))
        before = self.snapshot()
        self.run_install()
        self.assertEqual(before, self.snapshot())

    def test_identical_unowned_files_are_backed_up_before_adoption(self):
        self.write(self.doc / "SKILL.md", (self.source / "review/maintain-project-authorities/SKILL.md").read_bytes())
        self.run_install()
        self.assertTrue(list((self.home / ".agents/.workflow-ia-backups").rglob("SKILL.md")))

    def test_global_section_update_preserves_surrounding_bytes(self):
        prefix = b"\xef\xbb\xbf# Personal\r\n\r\n"
        suffix = "\r\n\r\n# SonarQube\r\nConserver les règles d'analyse.\r\n".encode("utf-8")
        self.write(self.instructions, prefix + installer.BEGIN + b"\r\nold block\r\n" + installer.END + suffix)
        self.run_install()
        source = self.source / "agents/GLOBAL_AGENTS_SECTION.md"
        expected = source.read_bytes().strip()
        self.assertEqual(self.instructions.read_bytes(), prefix + expected + suffix)
        updated = expected.replace(b"Shared Engineering", b"Common Engineering")
        self.assertNotEqual(updated, expected)
        self.write(source, updated + b"\n")
        before = self.snapshot()
        self.assertFalse(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)
        self.run_install()
        self.assertEqual(self.instructions.read_bytes(), prefix + updated + suffix)
        before = self.snapshot()
        self.assertTrue(self.run_install(check=True))
        self.run_install()
        self.assertEqual(self.snapshot(), before)

    def test_append_preserves_user_content_without_final_newline(self):
        personal = "Règles personnelles\r\n# SonarQube\r\nConserver les règles d'analyse.".encode("utf-8")
        self.write(self.instructions, personal)
        self.run_install()
        expected = (self.source / "agents/GLOBAL_AGENTS_SECTION.md").read_bytes().strip()
        self.assertEqual(self.instructions.read_bytes(), personal + b"\n\n" + expected + b"\n")

    def test_malformed_markers_fail_without_writes(self):
        for content in (installer.BEGIN, installer.END, installer.END + b"\n" + installer.BEGIN,
                        installer.BEGIN + b"\nx\n" + installer.END + b"\n" + installer.BEGIN,
                        b"inline " + installer.BEGIN + b"\nx\n" + installer.END,
                        b"<!-- workflow-ia:broken -->"):
            with self.subTest(content=content):
                self.write(self.instructions, content)
                before = self.snapshot()
                with self.assertRaises(installer.InstallError):
                    self.run_install()
                self.assertEqual(self.snapshot(), before)

    def test_override_is_explicit_conflict_without_writes(self):
        self.write(self.codex / "AGENTS.override.md", b"override")
        before = self.snapshot()
        for check in (False, True):
            with self.assertRaisesRegex(installer.InstallError, "may mask AGENTS.md"):
                self.run_install(check=check)
            self.assertEqual(self.snapshot(), before)

    def test_missing_source_prevents_all_writes(self):
        (self.source / installer.GUIDES[-1]).unlink()
        with self.assertRaisesRegex(installer.InstallError, "Missing or empty source"):
            self.run_install()
        self.assertFalse(self.home.exists())
        self.assertFalse(self.codex.exists())

    def test_invalid_toml_prevents_writes(self):
        self.write(self.source / "review/review-and-remediate/tests-reviewer.toml", b"invalid = [")
        with self.assertRaises(tomllib.TOMLDecodeError):
            self.run_install()
        self.assertFalse(self.home.exists())

    def test_broken_skill_reference_prevents_writes(self):
        skill = self.source / "review/maintain-project-authorities/SKILL.md"
        self.write(skill, skill.read_bytes() + b"\n[missing](references/missing.md)\n")
        with self.assertRaisesRegex(installer.InstallError, "Missing skill reference"):
            self.run_install()
        self.assertFalse(self.home.exists())

    def test_check_never_writes_and_detects_update(self):
        before = self.snapshot()
        self.assertFalse(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.home.exists())
        self.run_install()
        before = self.snapshot()
        self.assertTrue(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)
        self.write(self.source / "VERSION", b"3.0.0\n")
        before = self.snapshot()
        self.assertFalse(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)

    def test_local_managed_edit_is_conflict_before_other_updates(self):
        self.run_install()
        self.write(self.codex / "agents/tests-reviewer.toml", b"local edit")
        self.write(self.source / "VERSION", b"3.0.0\n")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Locally modified managed file"):
            self.run_install()
        self.assertEqual(self.snapshot(), before)

    def test_missing_managed_file_is_repaired(self):
        self.run_install()
        (self.doc / "SKILL.md").unlink()
        self.assertFalse(self.run_install(check=True))
        self.run_install()
        self.assertTrue(self.run_install(check=True))

    def test_obsolete_owned_file_removed_personal_file_retained(self):
        self.run_install()
        old = self.doc / "references/obsolete.md"
        self.write(old, b"old")
        manifest = self.doc / installer.MANIFEST
        state = json.loads(manifest.read_bytes())
        state["files"]["references/obsolete.md"] = installer.digest(b"old")
        self.write(manifest, json.dumps(state).encode())
        self.write(self.doc / "references/personal.md", b"keep")
        self.run_install()
        self.assertFalse(old.exists())
        self.assertEqual((self.doc / "references/personal.md").read_bytes(), b"keep")

    def test_unsafe_manifest_paths_rejected(self):
        for name in ("../outside.txt", "/outside.txt", "C:/outside.txt", "folder\\outside", "x/../outside", "NUL", "name."):
            with self.subTest(name=name):
                self.write(self.doc / installer.MANIFEST, json.dumps({"owner": installer.OWNER, "files": {name: "a" * 64}}).encode())
                before = self.snapshot()
                with self.assertRaises(installer.InstallError):
                    self.run_install()
                self.assertEqual(self.snapshot(), before)

    def test_malformed_manifest_rejected(self):
        self.write(self.doc / installer.MANIFEST, b"not json")
        with self.assertRaisesRegex(installer.InstallError, "Invalid ownership manifest"):
            self.run_install()

    def test_directory_file_conflict_detected_before_writes(self):
        (self.codex / "agents/tests-reviewer.toml").mkdir(parents=True)
        with self.assertRaisesRegex(installer.InstallError, "Expected regular file"):
            self.run_install()
        self.assertFalse(self.home.exists())

    def symlink(self, link, target, directory=False):
        link.parent.mkdir(parents=True, exist_ok=True)
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")

    def test_symlink_skill_root_is_not_followed(self):
        outside = self.base / "outside"
        self.write(outside / "sentinel", b"safe")
        self.symlink(self.doc, outside, directory=True)
        with self.assertRaisesRegex(installer.InstallError, "Linked/reparse"):
            self.run_install()
        self.assertEqual(list(outside.iterdir()), [outside / "sentinel"])

    def test_symlink_managed_file_is_not_followed(self):
        outside = self.base / "sentinel"
        self.write(outside, b"safe")
        self.symlink(self.instructions, outside)
        with self.assertRaisesRegex(installer.InstallError, "Linked/reparse"):
            self.run_install()
        self.assertEqual(outside.read_bytes(), b"safe")

    def test_broken_symlink_rejected(self):
        self.symlink(self.doc, self.base / "missing", directory=True)
        with self.assertRaisesRegex(installer.InstallError, "Linked/reparse"):
            self.run_install()

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_windows_junction_rejected(self):
        outside = self.base / "outside"
        self.write(outside / "sentinel", b"safe")
        self.doc.parent.mkdir(parents=True)
        # mklink is a cmd builtin; no deletion or moving is delegated across shells.
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.doc), str(outside)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.addCleanup(lambda: self.doc.rmdir())
        with self.assertRaisesRegex(installer.InstallError, "Linked/reparse"):
            self.run_install()
        self.assertEqual((outside / "sentinel").read_bytes(), b"safe")

    def test_atomic_replace_failure_preserves_previous_file(self):
        target = self.base / "file"
        self.write(target, b"original")
        with patch.object(installer.os, "replace", side_effect=OSError("simulated failure")):
            with self.assertRaisesRegex(OSError, "simulated"):
                installer.atomic_write(target, b"new")
        self.assertEqual(target.read_bytes(), b"original")
        self.assertFalse(list(target.parent.glob(".workflow-ia-*")))

    def test_backup_failure_prevents_managed_writes(self):
        self.write(self.doc / "SKILL.md", b"legacy")
        before = self.snapshot()
        with patch.object(installer, "atomic_write", side_effect=OSError("backup unavailable")):
            with self.assertRaises(OSError):
                self.run_install()
        self.assertEqual(before, self.snapshot())

    def test_user_paths_defaults_override_and_invalid_relative(self):
        with patch.object(installer.Path, "home", return_value=self.home), patch.dict(os.environ, {}, clear=True):
            self.assertEqual(installer.user_paths(), (self.home, self.home / ".codex"))
            os.environ["CODEX_HOME"] = str(self.codex)
            self.assertEqual(installer.user_paths(), (self.home, self.codex))
            for value in ("relative", "", str(self.home / ".." / "codex")):
                os.environ["CODEX_HOME"] = value
                with self.assertRaises(installer.InstallError):
                    installer.user_paths()

    def test_overlapping_source_destination_rejected(self):
        with self.assertRaisesRegex(installer.InstallError, "overlaps source"):
            installer.install(self.source, self.source, self.codex)

    def test_cli_from_unrelated_directory_with_isolated_home(self):
        env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home), CODEX_HOME=str(self.codex), PYTHONDONTWRITEBYTECODE="1")
        command = [sys.executable, "-B", str(self.source / "scripts/install.py")]
        def run(*args):
            return subprocess.run([*command, *args], cwd=self.base, env=env, capture_output=True, text=True)
        self.assertEqual(run("--check").returncode, 1)
        result = run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(run("--check").returncode, 0)
        self.write(self.codex / "AGENTS.override.md", b"override")
        self.assertEqual(run("--check").returncode, 2)


if __name__ == "__main__":
    unittest.main()
