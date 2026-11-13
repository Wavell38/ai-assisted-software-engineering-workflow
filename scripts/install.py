#!/usr/bin/env python3
"""Install the shared Codex workflow locally. Python 3.11+, standard library only."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import sys
import tempfile
import uuid

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or newer is required (TOML validation uses tomllib).")

import tomllib


SOURCE_ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("maintain-project-authorities", "review-and-remediate")
REVIEWERS = ("contract", "correctness", "tests", "architecture", "documentation")
GUIDES = (
    "DOCUMENTATION_MODEL.md",
    "adr/ADR_GUIDE.md",
    "architecture/ARCHITECTURE_GUIDE.md",
    "architecture/ARCHITECTURE_CHANGE_WORKFLOW.md",
    "codebase-map/CODEBASE_MAP_GUIDE.md",
    "contracts/CONTRACT_GUIDE.md",
    "qualification/QUALIFICATION_GUIDE.md",
    "roadmap/ROADMAP_GUIDE.md",
)
TEMPLATES = (
    "adr/ADR_TEMPLATE.md",
    "architecture/ARCHITECTURE_TEMPLATE.md",
    "codebase-map/CODEBASE_MAP_TEMPLATE.md",
    "contracts/CONTRACT_TEMPLATE.md",
    "qualification/QUALIFICATION_REPORT_TEMPLATE.md",
    "roadmap/ROADMAP_TEMPLATE.md",
    "roadmap/PHASE_PLAN_TEMPLATE.md",
)
INIT_RESOURCES = {
    "workflow_ia.py": "scripts/workflow_ia.py",
    "INIT_WORKFLOW.md": "INIT_WORKFLOW.md",
    "AGENTS_BASE_TEMPLATE.md": "agents/AGENTS_BASE_TEMPLATE.md",
    "VERSION": "VERSION",
}
MANIFEST = ".workflow-ia-managed.json"
OWNER = "workflow-ia"
BEGIN = b"<!-- workflow-ia:begin -->"
END = b"<!-- workflow-ia:end -->"


class InstallError(Exception):
    """A source, path, or ownership conflict that must not be silently repaired."""


def safe_path(path: Path) -> None:
    """Reject links (including Windows junctions/reparse points) in every component."""
    for part in reversed((path, *path.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise InstallError(f"Linked/reparse path is not supported: {part}")
        if part != path and not stat.S_ISDIR(info.st_mode):
            raise InstallError(f"Expected directory: {part}")


def read_file(path: Path) -> bytes | None:
    safe_path(path)
    if not path.exists():
        return None
    if not path.is_file():
        raise InstallError(f"Expected regular file: {path}")
    return path.read_bytes()


def source_file(root: Path, relative: str) -> bytes:
    content = read_file(root / relative)
    if content is None or not content.strip():
        raise InstallError(f"Missing or empty source resource: {relative}")
    content.decode("utf-8")
    return content


def validate_links(bundles: dict[str, dict[str, bytes]]) -> None:
    """Validate executable skill routes, not example consumer links in templates."""
    available = {f"{name}/{path}" for name, files in bundles.items() for path in files}
    for name, files in bundles.items():
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", files["SKILL.md"].decode("utf-8"))
        reached = set()
        for link in links:
            target = link.split("#", 1)[0]
            if not target:
                continue
            if ":" in target or "\\" in target or target.startswith("/"):
                raise InstallError(f"Non-relative skill reference: {name}: {link}")
            parts = [name]
            for part in target.split("/"):
                if part == "..":
                    if not parts:
                        raise InstallError(f"Escaping skill reference: {link}")
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            normalized = "/".join(parts)
            if normalized not in available:
                raise InstallError(f"Missing skill reference: {name}: {link}")
            reached.add(normalized)
        required = {f"{name}/{path}" for path in files if path.startswith(("references/", "assets/"))}
        if not required <= reached:
            raise InstallError(f"Unrouted resources in {name}: {sorted(required - reached)}")


def load_sources(root: Path) -> tuple[dict[str, dict[str, bytes]], dict[str, bytes], bytes]:
    version = source_file(root, "VERSION")
    if not re.fullmatch(rb"\d+\.\d+\.\d+\s*", version):
        raise InstallError("VERSION must contain one semantic version X.Y.Z")
    bundles = {
        name: {"SKILL.md": source_file(root, f"review/{name}/SKILL.md"), "VERSION": version}
        for name in SKILLS
    }
    for name, files in bundles.items():
        header = files["SKILL.md"].decode("utf-8").split("---", 2)
        if len(header) != 3 or header[0].strip() or f"name: {name}\n" not in header[1].replace("\r\n", "\n"):
            raise InstallError(f"Invalid skill frontmatter: {name}")
        if not re.search(r"^description: .+", header[1], re.MULTILINE):
            raise InstallError(f"Missing skill description: {name}")
    for path in GUIDES:
        bundles[SKILLS[0]][f"references/{path}"] = source_file(root, path)
    for path in TEMPLATES:
        bundles[SKILLS[0]][f"assets/{path}"] = source_file(root, path)
    reviewers = {}
    for role in REVIEWERS:
        name = f"{role}-reviewer.toml"
        content = source_file(root, f"review/{SKILLS[1]}/{name}")
        profile = tomllib.loads(content.decode("utf-8"))
        required = ("name", "description", "model", "model_reasoning_effort", "developer_instructions")
        if any(not isinstance(profile.get(key), str) or not profile[key].strip() for key in required):
            raise InstallError(f"Incomplete reviewer profile: {name}")
        if profile["name"] != f"{role}_reviewer" or profile.get("sandbox_mode") != "read-only":
            raise InstallError(f"Unexpected reviewer identity or sandbox: {name}")
        reviewers[name] = content
        bundles[SKILLS[1]][name] = content
    validate_links(bundles)
    block = source_file(root, "agents/GLOBAL_AGENTS_SECTION.md").strip()
    if merge_instructions(block, block) != block or not block.startswith(BEGIN) or not block.endswith(END):
        raise InstallError("Invalid global instruction block source")
    return bundles, reviewers, block


def merge_instructions(existing: bytes, block: bytes) -> bytes:
    """Change only the delimited block; preserve every byte outside it."""
    existing.decode("utf-8-sig")
    if b"<!-- workflow-ia:" not in existing:
        separator = b"" if not existing or existing.endswith(b"\n\n") else b"\n" if existing.endswith(b"\n") else b"\n\n"
        return existing + separator + block + b"\n"
    if existing.count(BEGIN) != 1 or existing.count(END) != 1 or existing.count(b"<!-- workflow-ia:") != 2:
        raise InstallError("Malformed or multiple workflow-ia markers in AGENTS.md")
    start, end = existing.index(BEGIN), existing.index(END) + len(END)
    prefix, suffix = existing[:start], existing[end:]
    if start >= end or (prefix and not prefix.endswith(b"\n") and prefix != b"\xef\xbb\xbf") or (suffix and not suffix.startswith((b"\n", b"\r\n"))):
        raise InstallError("Workflow-ia markers must be ordered and on their own lines")
    begin_tail = existing[start + len(BEGIN):]
    end_prefix = existing[:end - len(END)]
    if not begin_tail.startswith((b"\n", b"\r\n")) or not end_prefix.endswith(b"\n"):
        raise InstallError("Workflow-ia markers must be on their own lines")
    return prefix + block + suffix


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def valid_managed_name(name: str) -> bool:
    parts = PurePosixPath(name).parts
    return bool(parts) and "/".join(parts) == name and all(
        re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", part)
        and part.split(".")[0].upper() not in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(10)), *(f"LPT{i}" for i in range(10))}
        for part in parts
    )


def load_manifest(root: Path) -> dict[str, str]:
    raw = read_file(root / MANIFEST)
    if raw is None:
        return {}
    try:
        state = json.loads(raw)
        if set(state) != {"owner", "files"} or state["owner"] != OWNER or not isinstance(state["files"], dict):
            raise ValueError("unexpected manifest structure")
        for path, value in state["files"].items():
            if not valid_managed_name(path) or not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise ValueError("unsafe path or invalid hash")
        return state["files"]
    except (ValueError, TypeError) as exc:
        raise InstallError(f"Invalid ownership manifest {root / MANIFEST}: {exc}") from exc


def plan_bundle(root: Path, files: dict[str, bytes]) -> tuple[dict[Path, bytes | None], dict[Path, bytes]]:
    """Preflight managed files, retaining unrelated personal files in the same tree."""
    safe_path(root)
    old = load_manifest(root)
    changes, backups = {}, {}
    for name in sorted(old.keys() | files.keys()):
        path = root / name
        current = read_file(path)
        desired = files.get(name)
        if current is not None and name in old and digest(current) != old[name] and current != desired:
            raise InstallError(f"Locally modified managed file: {path}; preserve or reconcile it before retrying")
        if current is not None and name not in old:
            backups[path] = current
        if current != desired:
            changes[path] = desired
    manifest = (json.dumps({"owner": OWNER, "files": {name: digest(data) for name, data in sorted(files.items())}}, indent=2) + "\n").encode()
    if read_file(root / MANIFEST) != manifest:
        changes[root / MANIFEST] = manifest
    return changes, backups


def atomic_write(path: Path, content: bytes) -> None:
    safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_path(path)
    previous = path.stat() if path.exists() else None
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".workflow-ia-", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if previous:
            os.chmod(temporary, stat.S_IMODE(previous.st_mode))
        safe_path(path)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def launcher_files(home: Path, codex_home: Path, bin_dir: Path) -> dict[str, bytes]:
    """Preflight user PATH and generate a launcher independent of the source clone."""
    if not bin_dir.is_absolute() or ".." in bin_dir.parts or not bin_dir.is_relative_to(home) or bin_dir == home:
        raise InstallError("CLI bin directory must be an absolute directory below the user home")
    safe_path(bin_dir)
    paths = [os.path.normcase(os.path.abspath(part.strip('"'))) for part in os.get_exec_path() if part]
    if os.path.normcase(str(bin_dir)) not in paths:
        raise InstallError(f"CLI directory is not on PATH: {bin_dir}. Add it to your user PATH, reopen the terminal, and rerun; no PATH settings are changed by the installer.")
    name = "workflow-ia.cmd" if os.name == "nt" else "workflow-ia"
    target = bin_dir / name
    old = load_manifest(bin_dir)
    # Unlike documentary legacy adoption, an unowned executable is never replaced.
    if read_file(target) is not None and name not in old:
        raise InstallError(f"Unowned CLI command already exists: {target}; choose another --bin-dir or reconcile explicitly")
    if set(old) - {name}:
        raise InstallError(f"Unexpected CLI ownership entries in {bin_dir / MANIFEST}")
    variants = ("workflow-ia", "workflow-ia.exe", "workflow-ia.com", "workflow-ia.bat", "workflow-ia.ps1") if os.name == "nt" else ()
    for directory in [Path.cwd(), *(Path(p.strip('"')) for p in os.get_exec_path() if p)]:
        for variant in (name, *variants):
            candidate = directory / variant
            if candidate != target and os.path.lexists(candidate):
                raise InstallError(f"Conflicting CLI command: {candidate}; resolve PATH ambiguity before installing")
    script = codex_home / "workflow-ia/workflow_ia.py"
    if os.name == "nt":
        def quote(path: str) -> str:
            if any(char in path for char in ('"', '\n', '\r')):
                raise InstallError("Unsupported quote or newline in launcher path")
            return '"' + path.replace('%', '%%') + '"'
        content = f"@echo off\r\nsetlocal DisableDelayedExpansion\r\n{quote(sys.executable)} -B {quote(str(script))} %*\r\nexit /b %errorlevel%\r\n"
    else:
        content = f"#!/bin/sh\nexec {shlex.quote(sys.executable)} -B {shlex.quote(str(script))} \"$@\"\n"
    return {name: content.encode("utf-8")}


def install(source: Path, home: Path, codex_home: Path, *, check: bool = False,
            bin_dir: Path | None = None) -> bool:
    bundles, reviewers, block = load_sources(source)
    initialization = {target: source_file(source, path) for target, path in INIT_RESOURCES.items()}
    bin_dir = bin_dir or home / ".local/bin"
    roots = [home / ".agents" / "skills" / name for name in SKILLS] + [codex_home / "agents", codex_home / "workflow-ia", bin_dir]
    # Overlapping roots could overwrite source files or mix skills and reviewer ownership.
    for i, root in enumerate(roots):
        if root.is_relative_to(source) or source.is_relative_to(root):
            raise InstallError(f"Installation overlaps source repository: {root}")
        for other in roots[:i]:
            if root.is_relative_to(other) or other.is_relative_to(root):
                raise InstallError(f"Overlapping installation roots: {root} and {other}")
    launcher = launcher_files(home, codex_home, bin_dir)
    instructions = codex_home / "AGENTS.md"
    if instructions.is_relative_to(source):
        raise InstallError("CODEX_HOME must not be inside the source repository")
    safe_path(codex_home)
    override = codex_home / "AGENTS.override.md"
    safe_path(override)
    if override.exists():
        raise InstallError(f"{override} exists and may mask AGENTS.md. Reconcile the global instructions manually; no files were changed.")
    existing = read_file(instructions)
    updated = merge_instructions(existing or b"", block)
    plans = [plan_bundle(root, files) for root, files in zip(roots, [*bundles.values(), reviewers, initialization, launcher])]
    changes = {path: data for updates, _ in plans for path, data in updates.items()}
    executable = bin_dir / next(iter(launcher))
    needs_mode = os.name != "nt" and executable.exists() and not os.access(executable, os.X_OK)
    if existing != updated:
        changes[instructions] = updated
    backup_sets = [
        (root, home / ".agents" / ".workflow-ia-backups" if root in roots[:2] else codex_home / ".workflow-ia-backups", backup)
        for root, (_, backup) in zip(roots, plans) if backup
    ]
    if existing is not None and BEGIN not in existing and existing != updated:
        backup_sets.append((codex_home, codex_home / ".workflow-ia-backups", {instructions: existing}))
    # Check backup destinations before writing any managed file or creating a directory.
    for _, backup_root, _ in backup_sets:
        safe_path(backup_root)
        if backup_root.exists() and not backup_root.is_dir():
            raise InstallError(f"Expected backup directory: {backup_root}")
    if check:
        for path in changes:
            print(f"OUTDATED {path}")
        print("Installation is current." if not changes else "Installation requires an update.")
        if needs_mode:
            print(f"OUTDATED executable permission: {executable}")
        return not changes and not needs_mode
    for root, backup_root, backup in backup_sets:
        destination = backup_root / uuid.uuid4().hex / root.name
        for path, content in backup.items():
            atomic_write(destination / path.relative_to(root), content)
        print(f"BACKUP {destination}")
    for path, data in changes.items():
        if data is None:
            safe_path(path)
            path.unlink()
            print(f"REMOVE {path}")
        else:
            atomic_write(path, data)
            print(f"WRITE {path}")
    if os.name != "nt" and (executable in changes or needs_mode):
        executable.chmod(executable.stat().st_mode | 0o111)
    resolved = shutil.which("workflow-ia")
    if resolved is None or Path(resolved).resolve() != executable.resolve():
        raise InstallError(f"Installed CLI is not reachable as workflow-ia on PATH: {executable}")
    print(f"CLI {resolved}")
    print("Installation updated." if changes else "Installation is current; no changes.")
    return True


def user_paths() -> tuple[Path, Path]:
    home = Path.home()
    value = os.environ.get("CODEX_HOME")
    codex_home = Path(value).expanduser() if value is not None else home / ".codex"
    if not home.is_absolute() or not codex_home.is_absolute():
        raise InstallError("User home and CODEX_HOME must be absolute paths; relative/empty CODEX_HOME is ambiguous")
    if ".." in home.parts or ".." in codex_home.parts:
        raise InstallError("Home paths must not contain '..' components")
    return home, codex_home


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify installation without writing (exit 1 if outdated)")
    parser.add_argument("--bin-dir", type=Path, help="user directory already on PATH (default: ~/.local/bin)")
    args = parser.parse_args(argv)
    try:
        home, codex_home = user_paths()
        return 0 if install(SOURCE_ROOT, home, codex_home, check=args.check, bin_dir=args.bin_dir) else 1
    except (InstallError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Installation not completed. If an I/O failure occurred during writes, earlier files may have been updated; fix the cause and rerun.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
