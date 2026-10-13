# AGENTS.md — Project Base Template

> Authoring reference for ChatGPT, Codex, or a human drafting a project's `AGENTS.md`.
> Adapt to the actual repository; remove examples, placeholders, and irrelevant sections.
> Do not invent architectural decisions, commands, or project conventions.
> When Workflow IA is installed globally, its instructions already cover the shared skills,
> Git operations, recommended commit messages, and `.ai-history/**`; do not duplicate them.
> If a repository must also work without that installation, document its needs explicitly.

## Scope

These instructions apply to this repository unless a more specific `AGENTS.md` applies
within a subdirectory. Add nested `AGENTS.md` files only for genuinely distinct local rules.

## Project context

<!-- PROJECT-SPECIFIC: establish these facts from the repository or an explicit decision. -->

- Purpose and scope: `<what this repository does>`.
- Supported languages, runtimes, and toolchains: `<versions and sources of truth>`.
- Relevant entry points / subsystems: `<paths or links when helpful>`.
- Documentation language and conventions: `<only if not already evident>`.

## Architecture and project authorities

<!-- PROJECT-SPECIFIC: list existing authorities and accepted boundaries only.
     Omit missing document types; this template does not mandate creating them. -->

- Architecture: `<path, if present>`.
- Codebase map: `<path, if present>`.
- Roadmap / active phase: `<paths, if present>`.
- Contracts / ADRs / qualifications: `<paths or index, if present>`.
- Important module ownership, dependency constraints, or project-specific invariants:
  `<concise rules not already stated in a referenced authority>`.

Use these authorities as sources for their respective decisions and current project state.
Reference them instead of reproducing their contents here.

## Working and implementation rules

- Inspect relevant code, existing conventions, and applicable authorities before editing.
- Keep changes focused and preserve existing behavior unless the task requires otherwise.
- Organize production code around cohesive responsibilities and explicit ownership boundaries.
- Preserve accepted dependency directions and module boundaries.
- When modifying substantial handwritten code, reassess cohesion and split independent
  responsibilities where justified; do not use file length alone as a splitting rule.
- Avoid unnecessary abstractions, dependencies, layers, and speculative extensibility.
- Do not refactor unrelated or untouched legacy code solely for consistency.

## Correctness and compatibility

- Respect the project's dependency manifests, lockfiles, and supported toolchain versions.
- Preserve relevant contracts, invariants, units, precision, ordering, identity, and failure semantics.
- Make important failure cases explicit; do not silently discard or coerce evidence.
- Keep public interfaces appropriately typed when the language supports it.
- Never expose secrets or sensitive data; use safe defaults for external or destructive actions.

## Validation

<!-- PROJECT-SPECIFIC: replace with actual commands or remove unavailable checks. -->

- Formatting / lint: `<command>`.
- Type checking / static analysis: `<command, if applicable>`.
- Unit / integration tests: `<commands>`.
- Build / project-specific qualification: `<commands, if applicable>`.
- Important prerequisites, fixtures, or safety restrictions: `<details, if applicable>`.

Run relevant validation for changed behavior, revalidate after material corrections,
and report executed checks, missing checks, and remaining limitations.
Do not weaken failing tests just to obtain a passing result.

## Project-specific constraints

<!-- PROJECT-SPECIFIC: keep only permanent rules genuinely needed in this repository.
     Examples: ROS 2 / C++ ownership and QoS; Rust determinism; Unreal reflection/threading;
     database migration rules; hardware limits; regulated deployments. -->

- `<constraint, or remove this section>`.

## Protected paths

<!-- PROJECT-SPECIFIC: add only additional protected paths.
     Do not duplicate global `.ai-history/**` instructions. -->

- `<path or pattern>`: `<protection rule>`.
