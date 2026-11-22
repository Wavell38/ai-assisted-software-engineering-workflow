#!/usr/bin/env python3
"""Launch the installed Workflow IA initialization in the current terminal."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


GPT_62_SOL = "gpt-6.2-sol"


class InitError(Exception):
    """A prerequisite failed before starting the interactive session."""


def probe(command: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InitError(f"Cannot run {command[0]}: {exc}") from exc
    if result.returncode:
        raise InitError(f"Prerequisite failed ({result.returncode}): {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def repository_root(cwd: Path) -> Path:
    git = shutil.which("git")
    if not git:
        raise InitError("Git is required and must be on PATH.")
    # Ignore inherited Git routing variables: init always targets the caller's worktree.
    if any(key in os.environ for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR")):
        raise InitError("Unset GIT_DIR, GIT_WORK_TREE and GIT_COMMON_DIR before initialization.")
    if probe([git, "rev-parse", "--is-inside-work-tree"], cwd).strip() != "true":
        raise InitError("Run workflow-ia init inside a Git worktree (git init for a new project).")
    root = Path(probe([git, "rev-parse", "--show-toplevel"], cwd).strip()).resolve()
    if not root.is_dir() or not cwd.resolve().is_relative_to(root):
        raise InitError("Git returned an invalid worktree root.")
    return root


def codex_command(value: str | None) -> list[str]:
    found = shutil.which(value or "codex")
    if not found:
        # Explicit Python wrappers are useful for local integrations and simulated tests.
        found = value if value and Path(value).is_file() else None
    if not found:
        raise InitError("Codex is missing. Install/authenticate Codex separately and put it on PATH.")
    path = Path(found).resolve()
    if path.suffix.lower() == ".py":
        return [sys.executable, "-B", str(path)]
    if os.name == "nt" and path.suffix.lower() in (".cmd", ".bat", ".ps1"):
        # Bypass npm's batch shell: procedure text must remain one literal argument.
        entry = path.parent / "node_modules/@openai/codex/bin/codex.js"
        node = path.parent / "node.exe"
        runtime = str(node) if node.is_file() else shutil.which("node")
        if path.stem.lower() != "codex" or not entry.is_file() or not runtime:
            raise InitError("Unsupported Codex shell shim. Use --codex with a native executable or the standard npm installation.")
        return [runtime, str(entry)]
    return [str(path)]


def session_command(command: list[str], root: Path, resources: Path,
                    model: str, effort: str) -> list[str]:
    procedure = resources / "INIT_WORKFLOW.md"
    template = resources / "AGENTS_BASE_TEMPLATE.md"
    try:
        instructions = procedure.read_text(encoding="utf-8")
        if not instructions.strip() or not template.read_text(encoding="utf-8").strip():
            raise InitError("Initialization resources are empty; rerun the Workflow IA installer.")
    except (OSError, UnicodeError) as exc:
        raise InitError(f"Initialization resources unavailable; rerun the installer: {exc}") from exc
    # Load the procedure here, rather than hoping the model opens a referenced file.
    prompt = (f"Initialize this Git repository using the procedure from {procedure}. "
              f"The complete procedure is supplied in developer_instructions. "
              f"Use the project AGENTS authoring template at {template}. "
              "Start with analysis and clarification; await explicit framing validation before writing.")
    return [*command, "--model", model, "--config", f'model_reasoning_effort="{effort}"',
            "--config", "developer_instructions=" + json.dumps(instructions, ensure_ascii=False),
            "--cd", str(root), prompt]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init", help="analyze and frame a Git project interactively with Codex")
    init.add_argument("--model", default=GPT_62_SOL, help="explicit session model (no fallback)")
    init.add_argument("--reasoning-effort", default="xhigh", choices=("low", "medium", "high", "xhigh", "max", "ultra"))
    init.add_argument("--codex", help="explicit Codex executable or Python wrapper")
    args = parser.parse_args(argv)
    try:
        if sys.version_info < (3, 11):
            raise InitError("Python 3.11 or newer is required.")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", args.model):
            raise InitError("Invalid model identifier.")
        root = repository_root(Path.cwd())
        command = codex_command(args.codex)
        version = probe([*command, "--version"], root)
        match = re.search(r"codex-cli (\d+\.\d+\.\d+)(-[\w.-]+)?", version)
        installed = tuple(map(int, match[1].split("."))) if match else ()
        uses_gpt_62 = args.model in (GPT_62_SOL, "gpt-6.2-astra")
        minimum = (0, 166, 0) if uses_gpt_62 else (0, 146, 0)
        if not match or installed < minimum or (uses_gpt_62 and installed == minimum and match[2]):
            required_version = ".".join(map(str, minimum))
            raise InitError(f"Codex CLI {required_version} or newer is required for {args.model}; "
                            "no model or effort fallback is used.")
        help_text = probe([*command, "--help"], root)
        if any(option not in help_text for option in ("--model", "--config", "--cd", "[PROMPT]")):
            raise InitError("Codex CLI does not advertise the required interactive options.")
        launch = session_command(command, root, Path(__file__).resolve().parent,
                                 args.model, args.reasoning_effort)
        print(f"Workflow IA: {root}\nCodex: {args.model} / {args.reasoning_effort}", flush=True)
        # No pipes, input payload, new console, or detached session: preserve the terminal.
        result = subprocess.run(launch, cwd=root)
        if result.returncode:
            print(f"Codex exited with status {result.returncode}; initialization is not confirmed. No fallback was attempted.", file=sys.stderr)
        return result.returncode if result.returncode >= 0 else 128 - result.returncode
    except InitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: Cannot start Codex: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
