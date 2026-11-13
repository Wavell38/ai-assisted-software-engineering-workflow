"""Deterministic CLI acceptance; fake Codex never calls a model or personal state."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_install


installer = test_install.installer
REPO = test_install.REPO
spec = importlib.util.spec_from_file_location("workflow_ia", REPO / "scripts/workflow_ia.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

FAKE_CODEX = '''import json, os, pathlib, sys
if "--version" in sys.argv:
    print(os.environ.get("FAKE_VERSION", "codex-cli 0.146.0"))
elif "--help" in sys.argv:
    print(os.environ.get("FAKE_HELP", "codex --model --config --cd [PROMPT]"))
else:
    pathlib.Path(os.environ["FAKE_CAPTURE"]).write_text(json.dumps({
        "args": sys.argv[1:], "cwd": os.getcwd(),
        "codex_home": os.environ.get("CODEX_HOME")}), encoding="utf-8")
    print("READY", flush=True)
    if os.environ.get("FAKE_INTERACTIVE"):
        for line in sys.stdin:
            print("ECHO:" + line.strip(), flush=True)
            if line.strip() == "quit": break
    raise SystemExit(int(os.environ.get("FAKE_EXIT", "0")))
'''


class InitTests(unittest.TestCase):
    setUp = test_install.InstallationTests.setUp
    write = test_install.InstallationTests.write
    snapshot = test_install.InstallationTests.snapshot
    run_install = test_install.InstallationTests.run_install

    def prepare(self, existing=False):
        self.run_install()
        self.project = self.base / ("existing project é" if existing else "new project é")
        self.project.mkdir()
        self.env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home),
                        CODEX_HOME=str(self.codex), PYTHONDONTWRITEBYTECODE="1",
                        PYTHONIOENCODING="utf-8",
                        FAKE_CAPTURE=str(self.base / "capture.json"))
        subprocess.run(["git", "init", "--quiet", str(self.project)], env=self.env, check=True)
        if existing:
            self.write(self.project / "AGENTS.md", b"# Personal project rules\n")
            self.write(self.project / "app.py", b"print('hello')\n")
            self.write(self.project / "ARCHITECTURE.md", b"# Existing architecture\n")
        self.fake = self.base / "fake codex.py"
        self.write(self.fake, FAKE_CODEX.encode())
        self.write(self.codex / "config.toml", b"# personal config must remain unchanged\n")
        self.command = [str(Path(shutil.which("workflow-ia"))), "init", "--codex", str(self.fake)]

    def invoke(self, *args, cwd=None):
        return subprocess.run([*self.command, *args], cwd=cwd or self.project,
                              env=self.env, capture_output=True, text=True, encoding="utf-8", timeout=30)

    def capture(self):
        return json.loads((self.base / "capture.json").read_text(encoding="utf-8"))

    def test_acceptance_new_and_light_existing_repositories(self):
        self.prepare()
        # The installed command must survive removal of its original source clone.
        shutil.rmtree(self.source)
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    self.write(self.project / "app.py", b"print('hello')\n")
                    self.write(self.project / "AGENTS.md", b"# Preserve personal rules\n")
                    self.write(self.project / "ROADMAP.md", b"# Preserve roadmap\n")
                before = {p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
                nested = self.project / "nested directory"
                nested.mkdir(exist_ok=True)
                result = self.invoke(cwd=nested)
                self.assertEqual(result.returncode, 0, result.stderr)
                data = self.capture()
                self.assertEqual(Path(data["cwd"]), self.project)
                self.assertEqual(data["codex_home"], str(self.codex))
                args = data["args"]
                self.assertNotIn("exec", args)
                self.assertEqual(args[args.index("--model") + 1], "gpt-6.1-sol")
                self.assertEqual(Path(args[args.index("--cd") + 1]), self.project)
                configs = [args[i+1] for i, arg in enumerate(args[:-1]) if arg == "--config"]
                self.assertIn('model_reasoning_effort="xhigh"', configs)
                injected = next(x.split("=", 1)[1] for x in configs if x.startswith("developer_instructions="))
                self.assertEqual(json.loads(injected), (self.codex / "workflow-ia/INIT_WORKFLOW.md").read_text(encoding="utf-8"))
                self.assertIn(str(self.codex / "workflow-ia/AGENTS_BASE_TEMPLATE.md"), args[-1])
                self.assertEqual({p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}, before)
                self.assertEqual((self.codex / "config.toml").read_bytes(), b"# personal config must remain unchanged\n")

    def test_continuous_terminal_streams_and_exit_status(self):
        self.prepare(existing=True)
        self.env.update(FAKE_INTERACTIVE="1", FAKE_EXIT="23")
        process = subprocess.Popen(self.command, cwd=self.project, env=self.env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, encoding="utf-8")
        def cleanup():
            if process.poll() is None:
                process.communicate("quit\n", timeout=20)
            for stream in (process.stdin, process.stdout, process.stderr):
                stream.close()
        self.addCleanup(cleanup)
        self.assertIn("Workflow IA:", process.stdout.readline())
        self.assertIn("gpt-6.1-sol / xhigh", process.stdout.readline())
        self.assertEqual(process.stdout.readline().strip(), "READY")
        for value in ("first response", "quit"):
            process.stdin.write(value + "\n")
            process.stdin.flush()
            self.assertEqual(process.stdout.readline().strip(), "ECHO:" + value)
        _, stderr = process.communicate(timeout=20)
        self.assertEqual(process.returncode, 23)
        self.assertIn("No fallback", stderr)

    def test_explicit_session_configuration(self):
        self.prepare()
        result = self.invoke("--model", "explicit-model", "--reasoning-effort", "high")
        self.assertEqual(result.returncode, 0, result.stderr)
        args = self.capture()["args"]
        self.assertIn("explicit-model", args)
        self.assertIn('model_reasoning_effort="high"', args)

    def test_absent_incompatible_and_failed_codex(self):
        self.prepare()
        result = self.invoke("--codex", str(self.base / "missing.exe"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("Codex is missing", result.stderr)
        for key, value in (("FAKE_VERSION", "codex-cli 0.100.0"), ("FAKE_HELP", "old CLI")):
            with self.subTest(key=key):
                self.env[key] = value
                self.assertEqual(self.invoke().returncode, 2)
                self.assertFalse((self.base / "capture.json").exists())
                del self.env[key]
        self.env["FAKE_EXIT"] = "41"
        self.assertEqual(self.invoke().returncode, 41)

    def test_non_repository_and_inherited_git_routing(self):
        self.prepare()
        self.assertEqual(self.invoke(cwd=self.base).returncode, 2)
        self.env["GIT_WORK_TREE"] = str(self.project)
        self.assertIn("Unset GIT_DIR", self.invoke().stderr)

    def test_missing_resource_fails_before_session(self):
        self.prepare()
        (self.codex / "workflow-ia/INIT_WORKFLOW.md").unlink()
        result = self.invoke()
        self.assertEqual(result.returncode, 2)
        self.assertIn("resources unavailable", result.stderr)
        self.assertFalse((self.base / "capture.json").exists())

    def test_path_not_present_and_unowned_command_conflict_write_nothing(self):
        before = self.snapshot()
        with patch.dict(os.environ, {"PATH": str(self.base / "different bin")}):
            with self.assertRaisesRegex(installer.InstallError, "not on PATH"):
                self.run_install()
        self.assertEqual(self.snapshot(), before)
        name = "workflow-ia.cmd" if os.name == "nt" else "workflow-ia"
        self.write(self.bin / name, b"personal executable")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Unowned CLI"):
            self.run_install()
        self.assertEqual(self.snapshot(), before)

    def test_shadowing_command_and_external_bin_rejected(self):
        other = self.base / "other bin"
        self.write(other / "workflow-ia", b"existing command")
        with patch.dict(os.environ, {"PATH": str(other) + os.pathsep + os.environ["PATH"]}):
            with self.assertRaisesRegex(installer.InstallError, "Conflicting CLI"):
                self.run_install()
        with self.assertRaisesRegex(installer.InstallError, "below the user home"):
            installer.install(self.source, self.home, self.codex, bin_dir=other)

    def test_new_resources_update_conflict_and_check_without_writes(self):
        self.run_install()
        self.write(self.source / "INIT_WORKFLOW.md", b"# Updated initialization procedure\n")
        before = self.snapshot()
        self.assertFalse(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)
        self.run_install()
        self.assertEqual((self.codex / "workflow-ia/INIT_WORKFLOW.md").read_bytes(), b"# Updated initialization procedure\n")
        self.write(self.codex / "workflow-ia/INIT_WORKFLOW.md", b"local edit")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Locally modified"):
            self.run_install()
        self.assertEqual(self.snapshot(), before)

    def test_final_launch_inherits_terminal_and_interrupt(self):
        self.prepare()
        with patch.object(cli, "repository_root", return_value=self.project), \
             patch.object(cli, "codex_command", return_value=["fake"]), \
             patch.object(cli, "probe", side_effect=["codex-cli 0.146.0", "--model --config --cd [PROMPT]"] * 2), \
             patch.object(cli, "session_command", return_value=["fake", "prompt"]), \
             patch.object(cli.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["init"]), 0)
            run.assert_called_once_with(["fake", "prompt"], cwd=self.project)
            run.side_effect = KeyboardInterrupt
            self.assertEqual(cli.main(["init"]), 130)

    @unittest.skipIf(os.name == "nt", "POSIX executable permissions")
    def test_missing_executable_permission_is_repaired_and_check_never_writes(self):
        self.run_install()
        executable = self.bin / "workflow-ia"
        executable.chmod(0o644)
        before = self.snapshot()
        self.assertFalse(self.run_install(check=True))
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(os.access(executable, os.X_OK))
        self.run_install()
        self.assertTrue(os.access(executable, os.X_OK))


if __name__ == "__main__":
    unittest.main()
