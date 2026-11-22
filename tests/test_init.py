"""Deterministic CLI acceptance; fake Codex never calls a model or personal state.

Instruction checks establish presence and routing, not compliance by a real model.
"""

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
    print(os.environ.get("FAKE_VERSION", "codex-cli 0.166.0"))
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

    def injected_instructions(self):
        args = self.capture()["args"]
        configs = [args[i+1] for i, arg in enumerate(args[:-1]) if arg == "--config"]
        injected = next(x.split("=", 1)[1] for x in configs if x.startswith("developer_instructions="))
        return json.loads(injected)

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
                self.assertEqual(args[args.index("--model") + 1], "gpt-6.2-sol")
                self.assertEqual(Path(args[args.index("--cd") + 1]), self.project)
                configs = [args[i+1] for i, arg in enumerate(args[:-1]) if arg == "--config"]
                self.assertIn('model_reasoning_effort="xhigh"', configs)
                self.assertEqual(self.injected_instructions(), (self.codex / "workflow-ia/INIT_WORKFLOW.md").read_text(encoding="utf-8"))
                self.assertIn(str(self.codex / "workflow-ia/AGENTS_BASE_TEMPLATE.md"), args[-1])
                self.assertEqual({p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}, before)
                self.assertEqual((self.codex / "config.toml").read_bytes(), b"# personal config must remain unchanged\n")

    def test_new_project_architecture_instructions_reach_installed_session(self):
        self.prepare()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        instructions = " ".join(self.injected_instructions().split())
        # Presence in the injected procedure is evidence of routing, not model behavior.
        for rule in (
            "identifier le modèle le plus approprié aux besoins et contraintes établis",
            "Présenter une recommandation par défaut avec les raisons déterminantes",
            "les alternatives réellement pertinentes et leurs principaux compromis",
            "Permettre à l'utilisateur d'accepter ou de modifier cette proposition",
            "ne pas lui demander systématiquement de choisir un modèle technique abstrait",
            "un monolithe modulaire est souvent pertinent si plusieurs responsabilités stables sont identifiées",
            "Un petit utilitaire ou un projet peu complexe peut justifier une structure plus simple",
            "Cette préférence n'est ni universelle ni une exigence implicite",
            "ROS 2, embarqué, ECS, événementiel ou services distribués restent sélectionnables",
            "responsabilités, frontières et directions de dépendance importantes, au-delà du nom du modèle",
            "Distinguer architecture de déploiement, organisation interne du code et organisation des agents IA",
            "Ne pas imposer de couches, interfaces, packages, sous-agents ou `AGENTS.md` imbriqués sans nécessité démontrée",
            "**Attendre la réponse humaine avant de créer, modifier ou supprimer un document**",
            "Consigner la décision architecturale acceptée dans `ARCHITECTURE.md`",
            "ne pas inventer de modules physiques, de chemins ou de codebase map",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, instructions)
        self.assertFalse((self.project / "CODEBASE_MAP.md").exists())

    def test_existing_project_architecture_instructions_are_routed(self):
        self.prepare(existing=True)
        architecture = (self.project / "ARCHITECTURE.md").read_bytes()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.project / "ARCHITECTURE.md").read_bytes(), architecture)
        instructions = " ".join(self.injected_instructions().split())
        for rule in (
            "identifier d'abord les contraintes, conventions, frontières et responsabilités établies dans les autorités et le code",
            "Préserver l'architecture existante lorsqu'elle est acceptée et suffisamment identifiable",
            "Toute migration ou modification significative du modèle exige une proposition explicite, justifiée et validée",
            "ne jamais l'introduire silencieusement pendant l'initialisation",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, instructions)

    def test_contextual_adr_routing_instructions_are_distributed(self):
        self.prepare()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        instructions = " ".join(self.injected_instructions().split())
        for rule in (
            "`AGENTS.md` référence principalement les autorités générales et les emplacements documentaires",
            "`ARCHITECTURE.md` référence les ADR pertinents pour ses décisions",
            "`CODEBASE_MAP.md` référence les ADR ou contrats pertinents pour les responsabilités qu'il route",
            "Chaque ADR conserve sa décision et sa justification dans son propre fichier",
            "Éviter l'énumération systématique des ADR individuels dans `AGENTS.md`",
            "un lien direct reste utile lorsqu'une décision transversale gouverne les travaux concernés",
            "Ne pas créer d'index ADR supplémentaire sans besoin concret",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, instructions)
        template = " ".join((self.codex / "workflow-ia/AGENTS_BASE_TEMPLATE.md").read_text(encoding="utf-8").split())
        self.assertIn("Contracts / ADRs / qualifications: `<documentation locations, if present>`", template)
        self.assertIn("link an individual ADR here when a cross-cutting decision governs work in this scope", template)
        self.assertIn("rather than listing every ADR", template)

    def test_language_selection_instructions_reach_installed_session(self):
        self.prepare()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        instructions = " ".join(self.injected_instructions().split())
        # These are checks of the supplied instructions, not simulated model decisions.
        for rule in (
            "Pour un dépôt neuf sans convention établie, demander la langue documentaire",
            "en proposant **English** par défaut",
            "ne vaut pas choix accepté sans réponse de l'utilisateur",
            "Pour un dépôt existant, rechercher d'abord les conventions explicitement définies",
            "examiner la cohérence des usages documentaires existants",
            "la conserver ou la proposer dans le cadrage sans imposer de question supplémentaire",
            "En l'absence de convention identifiable, demander la préférence",
            "en cas d'ambiguïtés ou de conventions contradictoires, demander une clarification",
            "Distinguer la langue de communication avec l'utilisateur de la langue des autorités",
            "Inclure la langue retenue et sa source dans le cadrage soumis à validation",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, instructions)

    def test_language_persistence_and_generation_instructions_are_routed(self):
        self.prepare(existing=True)
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        instructions = " ".join(self.injected_instructions().split())
        template = " ".join((self.codex / "workflow-ia/AGENTS_BASE_TEMPLATE.md").read_text(encoding="utf-8").split())
        self.assertIn(str(self.codex / "workflow-ia/AGENTS_BASE_TEMPLATE.md"), self.capture()["args"][-1])
        self.assertIn("la consigner explicitement dans le `AGENTS.md` du projet pour les futures modifications documentaires", instructions)
        self.assertIn("même si elle paraît déjà évidente", instructions)
        self.assertIn("Documentation language: `<selected documentation language>`", template)
        self.assertIn("apply it consistently to future documentation changes", template)
        self.assertIn("The conversation language may differ", template)
        self.assertIn("including headings; this template's source language does not determine that choice", template)
        for authority in ("`AGENTS.md`", "`ARCHITECTURE.md`", "`ROADMAP.md`", "`CODEBASE_MAP.md`", "ADR", "contrats", "plans de phase"):
            with self.subTest(authority=authority):
                self.assertIn(authority, instructions)
        self.assertIn("adapter le contenu final généré à la convention du projet", instructions)
        self.assertIn("Ne pas traduire automatiquement l'ensemble de la documentation", instructions)
        self.assertIn("une migration linguistique globale exige une décision explicite", instructions)

    def test_optional_provenance_instructions_and_launcher_preservation(self):
        self.prepare(existing=True)
        self.write(self.project / ".gitignore", b"# Personal exclusions\n/build/\n")
        self.write(self.project / "ROADMAP.md", b"# Existing roadmap\n")
        for archive_exists in (False, True):
            with self.subTest(archive_exists=archive_exists):
                if archive_exists:
                    self.write(self.project / ".ai-history/legacy.md", b"legacy provenance fixture\n")
                before = {p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
                result = self.invoke()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((self.project / ".ai-history").exists(), archive_exists)
                self.assertEqual({p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}, before)
                instructions = " ".join(self.injected_instructions().split())
                for rule in (
                    "règles globales relatives à `.ai-history/**`",
                    "présence d'une archive, de l'installation de `prompts_archiver` et de son activation effective pour ce dépôt",
                    "Ces quatre éléments sont distincts",
                    "une archive existante ne prouve ni l'installation de l'outil ni son activation actuelle",
                    "l'installation ne prouve pas l'activation",
                    "Ne jamais supposer l'outil installé ou activé",
                    "ne pas installer ni activer `prompts_archiver`, ne pas créer `.ai-history/`",
                    "ne pas modifier `.gitignore` au seul motif que l'outil pourrait être utilisé",
                    "Ne pas ajouter de règles redondantes dans le `AGENTS.md` projet lorsque les règles globales suffisent",
                    "Ne pas modifier les autorités architecturales ou de planification",
                    "Ne pas introduire de question obligatoire sur cet outil",
                    "configuration explicite accessible hors de l'archive",
                    "ne pas déduire un état actif ou inactif ni chercher dans l'archive",
                ):
                    with self.subTest(rule=rule):
                        self.assertIn(rule, instructions)
        template = (self.codex / "workflow-ia/AGENTS_BASE_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("do not duplicate them", template)
        self.assertIn("Do not duplicate global `.ai-history/**` instructions", template)
        global_instructions = self.instructions.read_text(encoding="utf-8")
        history_rules = global_instructions.split("## AI History\n", 1)[1].split("<!-- workflow-ia:end -->", 1)[0]
        for rule in history_rules.splitlines():
            if rule.startswith("- "):
                self.assertNotIn(rule[2:], template)

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
        self.assertIn("gpt-6.2-sol / xhigh", process.stdout.readline())
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
        for model, version in (("gpt-6.2-astra", "0.166.0"), ("explicit-model", "0.146.0")):
            with self.subTest(model=model, version=version):
                self.env["FAKE_VERSION"] = f"codex-cli {version}"
                result = self.invoke("--model", model, "--reasoning-effort", "high")
                self.assertEqual(result.returncode, 0, result.stderr)
                args = self.capture()["args"]
                self.assertEqual(args[args.index("--model") + 1], model)
                self.assertIn('model_reasoning_effort="high"', args)

    def test_gpt_62_requires_codex_cli_0_166_0(self):
        self.prepare()
        for version in ("0.165.0", "0.166.0-alpha.1"):
            self.env["FAKE_VERSION"] = f"codex-cli {version}"
            for model_args in ((), ("--model", "gpt-6.2-astra")):
                with self.subTest(version=version, model_args=model_args):
                    result = self.invoke(*model_args)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("Codex CLI 0.166.0 or newer is required", result.stderr)
                    self.assertFalse((self.base / "capture.json").exists())

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
        result = self.invoke()
        self.assertEqual(result.returncode, 41)
        self.assertEqual(result.stdout.splitlines().count("READY"), 1)
        self.assertIn("No fallback was attempted", result.stderr)

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
             patch.object(cli, "probe", side_effect=["codex-cli 0.166.0", "--model --config --cd [PROMPT]"] * 2), \
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
