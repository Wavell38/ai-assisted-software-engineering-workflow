# AGENTS.md — Base Template

> Copy this file into a new repository, then adapt or remove the sections marked
> `PROJECT-SPECIFIC`. Keep the permanent rules concise; detailed architecture and
> framework guidance should live in authoritative project documentation.

## Scope

These instructions apply to the entire repository unless a more specific `AGENTS.md`
exists deeper in the tree.

## Communication

- Use the language requested by the user for progress updates, explanations, and final reports.
- Keep repository documentation in the project's established documentation language.
- Report uncertainty, blockers, validation results, and residual risks explicitly.

## Working principles

- Keep changes focused, explicit, reviewable, and proportional to the task.
- Prefer the simplest implementation that fully satisfies the current contract.
- Preserve existing behavior unless the task requires a change.
- Do not perform unrelated cleanup during a focused task.
- Do not introduce abstractions, layers, dependencies, configuration, or indirection without a demonstrated need.
- Treat repository authorities (`AGENTS.md`, architecture docs, ADRs, contracts, module guidance) as stronger than historical implementation patterns when they conflict.
- Inspect the relevant existing code before implementing; reuse established abstractions when they genuinely fit.

## Engineering rules

- Organize production code around cohesive responsibilities and explicit ownership boundaries.
- Preserve the project's established architectural model and dependency direction.
- Do not let one source unit accumulate independent responsibilities merely because they contribute to the same high-level feature.
- When one concept requires several cohesive implementation units, prefer a package/directory representing that concept rather than scattering unrelated sibling modules.
- Apply the same cohesion assessment recursively inside existing packages: when sibling modules form a stable, nameable sub-responsibility, consider grouping them into a nested package.
- Let directory depth follow cohesive responsibility boundaries, not file-count or line-count targets; do not keep a package artificially flat or add nesting only to reduce sibling count.
- Prefer paths and filenames that make ownership and likely contents predictable without opening unrelated files.
- Treat unusually large files, classes, and functions as signals requiring an explicit decomposition assessment, not as automatic violations.
- Prefer decomposition when it reduces unrelated context, coupling, or the amount of code that must be understood together.
- Do not create abstractions, layers, directories, classes, or interfaces solely to reduce line count.
- Apply these rules to new or materially changed production code; do not refactor untouched legacy code solely for structural consistency.
- Do not preserve a legacy layout solely for consistency when new or materially changed code has clearer cohesive boundaries.
- Reassess the structure of substantial new or materially changed code before considering implementation complete.

## Code quality

- Write clear, idiomatic code for the repository's supported language and toolchain versions.
- Prefer stable modern language and standard-library features when they materially improve clarity, safety, correctness, or maintainability.
- Avoid deprecated compatibility patterns and avoid novelty for novelty's sake.
- Keep public and non-trivial interfaces explicitly typed where the language/toolchain supports it.
- Prefer focused functions and explicit data flow over hidden state and implicit coupling.
- Make failure modes explicit; do not silently ignore malformed input or invariant violations.
- Avoid speculative generic frameworks and premature extensibility.
- Add comments only when they explain a non-obvious constraint, invariant, trade-off, or external requirement.
- Keep public APIs minimal and intentional.

## Architecture

<!-- PROJECT-SPECIFIC: replace or remove this section. -->

- Architectural model: `<e.g. layered / hexagonal / modular monolith / ROS 2 packages / ECS / other>`.
- Preserve the dependency direction and ownership boundaries defined in `<architecture authority>`.
- Business/domain rules belong in their designated ownership layer; infrastructure and framework details must not leak inward unless explicitly allowed.
- Prefer extending an existing coherent boundary over creating a parallel competing abstraction.

## Dependencies and compatibility

- Treat the repository's dependency manifests and lockfiles as authoritative.
- Do not upgrade language runtimes, frameworks, libraries, toolchains, or lockfiles unless the task requires it.
- Verify behavior against the exact supported/installed stable version; do not assume preview, nightly, beta, RC, or another release behaves identically.
- Prefer public supported APIs over private or internal implementation details.
- Add a dependency only when its value outweighs the maintenance, security, portability, and complexity cost.

## Correctness and data integrity

- Preserve domain invariants, ordering semantics, identity rules, units, precision, and boundary conditions.
- Distinguish missing/unknown data from valid zero or empty values.
- Do not silently repair, coerce, interpolate, discard, or reorder evidence unless the project contract explicitly defines that behavior.
- Prefer deterministic and reproducible behavior where the domain permits it.
- Make assumptions explicit when exact evidence is unavailable.

## Security and safety

- Never create, expose, log, or commit secrets, credentials, private keys, tokens, or sensitive production data.
- Use least privilege and safe local/test defaults.
- Do not enable destructive, production, deployment, external-execution, or live-operation behavior unless explicitly authorized.
- Treat external input as untrusted at relevant boundaries.

## Testing and validation

- Add or update tests for behavioral changes and material bug fixes.
- Test behavior, contracts, invariants, edge cases, and failure paths rather than implementation details alone.
- Do not weaken, delete, skip, or rewrite a failing test merely to obtain a green result.
- Run the smallest relevant checks during development and the complete project baseline before reporting completion.
- Re-run affected validations after remediation or structural refactoring.
- Report the commands executed, their results, and any validation that could not be completed.

### PROJECT-SPECIFIC validation baseline

```text
<lint command>
<format/check command>
<type/static-analysis command, if applicable>
<test command>
<dependency/build/integration checks, if applicable>
```

## Performance and concurrency

<!-- PROJECT-SPECIFIC: keep only when relevant. -->

- Do not optimize without a demonstrated requirement or measured bottleneck.
- Preserve bounded resource use where data volume can grow with input size.
- Make concurrency ownership, ordering, cancellation, and failure semantics explicit.
- Prefer correctness and observability over clever micro-optimizations.

## Documentation

- Update authoritative documentation when behavior, contracts, architecture, interfaces, operational procedures, or accepted project state changes.
- Keep durable design knowledge in project documentation rather than repeating it in task prompts.
- Use roadmap/codebase-map/document links as context routers when available; read specialized authorities only when they are relevant to the current task instead of bulk-reading unrelated documentation.
- Do not document an implementation as accepted until the corresponding evidence and validation exist.

## Repository hygiene

- Keep generated outputs, caches, local runtime state, large datasets, credentials, and temporary artifacts out of version control unless explicitly versioned by project policy.
- Preserve existing file-format, naming, and repository conventions when they remain compatible with current authorities.
- Do not modify unrelated files merely for formatting or stylistic consistency.

## Git discipline

- Do not commit.
- Do not tag.
- Do not push.
- Do not rewrite history or alter remotes unless explicitly authorized.
- Keep the working tree changes attributable to the current task easy to identify and review.
- Include a concise recommended commit message in the final report.

## Framework / domain rules

<!-- PROJECT-SPECIFIC: add only concise permanent rules that every relevant task must obey.
Examples:
- Python / FastAPI / Django conventions
- C++ language standard, compiler and ownership rules
- ROS 2 package/node/executor/QoS conventions
- Unreal Engine threading/reflection constraints
- database/migration rules
- trading/research integrity rules
Detailed guidance should live in dedicated authoritative docs. -->

## Ignore / protected areas

- `.ai-history/**`: versioned prompt/report archive. Do not read, search, modify, or use
  it as authority unless the current task explicitly concerns AI history, prompt
  evaluation, or archive maintenance.

<!-- PROJECT-SPECIFIC: add other directories that agents must not read, search, modify,
or treat as authority unless the task explicitly concerns them. -->

- `<path or pattern>`: `<rule>`
