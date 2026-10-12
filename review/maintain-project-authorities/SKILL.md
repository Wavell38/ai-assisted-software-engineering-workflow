---
name: maintain-project-authorities
description: Create, semantically update, verify, or compact structured project authorities using bundled documentary guidance. Use for ROADMAP.md, CODEBASE_MAP.md, ARCHITECTURE.md, phase plans, contracts, ADRs, qualification reports, and equivalent authorities, including small semantic updates.
---

# Maintain project authorities

Use this skill to apply the bundled documentation model consistently. This skill supplies
the procedure and documentary policy; accepted project facts remain in the project's
authorities. Explicit project rules govern project-specific adaptations.

## 1. Establish the documentation scope

- Read the applicable `AGENTS.md` first.
- Identify every structured authority the task may create or change.
- Establish the current-task diff/baseline when maintaining existing documents.
- If no accepted project fact owned by a document changed, do not edit that document merely
  because implementation work occurred.

## 2. Load only the policy needed

Resolve the following paths relative to this installed skill, never to the consumer
repository or current working directory. Load progressively:

1. [documentation model](references/DOCUMENTATION_MODEL.md);
2. the guide for each target document type;
3. the corresponding template only when creating a document, materially restructuring it,
   or when the guide explicitly requires it;
4. only the project authorities, code, phase state, or evidence needed to establish the facts
   being written.

| Target | Guide | Template (only when needed) |
| --- | --- | --- |
| Architecture | [guide](references/architecture/ARCHITECTURE_GUIDE.md), [change workflow](references/architecture/ARCHITECTURE_CHANGE_WORKFLOW.md) | [template](assets/architecture/ARCHITECTURE_TEMPLATE.md) |
| Codebase map | [guide](references/codebase-map/CODEBASE_MAP_GUIDE.md) | [template](assets/codebase-map/CODEBASE_MAP_TEMPLATE.md) |
| ADR | [guide](references/adr/ADR_GUIDE.md) | [template](assets/adr/ADR_TEMPLATE.md) |
| Contract | [guide](references/contracts/CONTRACT_GUIDE.md) | [template](assets/contracts/CONTRACT_TEMPLATE.md) |
| Roadmap and phase plan | [guide](references/roadmap/ROADMAP_GUIDE.md) | [roadmap](assets/roadmap/ROADMAP_TEMPLATE.md), [phase plan](assets/roadmap/PHASE_PLAN_TEMPLATE.md) |
| Qualification | [guide](references/qualification/QUALIFICATION_GUIDE.md) | [report](assets/qualification/QUALIFICATION_REPORT_TEMPLATE.md) |

This repository assembles these directories at installation time. When maintaining the
workflow source itself, resolve `references/DOCUMENTATION_MODEL.md` to the repository
root, and strip `references/` or `assets/` from the other paths to locate their source.
Templates contain example project links to adapt when creating an authority.

Consumer repositories need no copy under `docs/engineering/`. If existing project
instructions still select such a historical copy, report the migration boundary and
follow the explicit project policy; do not silently mix it with the global corpus.

Do not bulk-read unrelated documentation. Do not treat templates, this skill, execution
reports, or other workflow-repository material as project decisions.

If a required guide declared by this convention is missing, do not silently substitute an
unrelated document. Use the available project authority directly when sufficient; otherwise
report the missing policy source when it materially affects the task.

## 3. Classify information before writing it

Route each durable fact to the authority that owns the question:

- working rules -> applicable `AGENTS.md`;
- accepted system structure, boundaries, dependency direction, major flows -> architecture;
- where stable responsibilities live -> codebase map;
- why a durable non-trivial decision exists -> ADR;
- what must be true now -> contract;
- project trajectory, phase state, gate, next work -> roadmap;
- complex phase-local scope, sequencing, temporary state -> phase plan;
- durable evidence, measurements, reproduction, verdict -> qualification report;
- run narrative, prompt/report provenance -> execution report or `.ai-history/**` when enabled.

If a material fact has no valid owner or applicable authorities conflict, do not invent a new
project rule silently. Report the gap or block for a design decision when required.

## 4. Preserve document semantics

For living authorities, write the **current accepted state**, not an append-only history:

- replace superseded state instead of appending chronology;
- remove stale statements that the new accepted state makes false or redundant;
- keep the document at the abstraction level owned by its guide;
- route detail to the specialized authority rather than duplicating it;
- keep changes focused on facts affected by the current task.

ADRs and qualification reports are durable records rather than ordinary living-state
projections. Do not silently rewrite historical decisions or terminal evidence; supersede,
extend, or add a new record according to the applicable guide.

Phase plans may evolve while active, but must not become copies of global authorities or
qualification reports.

## 5. Apply the target guide

Follow the applicable guide rather than reproducing all document-specific rules here. In
particular:

- roadmap entries stay compact and route detailed phase state elsewhere;
- codebase maps describe current stable routing/ownership, not phase or implementation history;
- architecture describes accepted conceptual structure, not roadmap progress;
- contracts contain current normative behavior, while rationale belongs in ADRs;
- qualifications preserve evidence and its limits without becoming contracts or roadmaps.

These examples do not override the bundled guides or explicit project rules.

## 6. Verify the result

Before completion, check that:

- every changed statement belongs to the target authority;
- superseded living state was replaced rather than accumulated;
- the same normative fact was not copied into multiple authorities;
- links and routed references point to the appropriate detailed source;
- accepted-state claims are supported by the repository state/evidence required by policy;
- no unrelated documentation cleanup was introduced;
- available deterministic documentation checks are run when repository policy requires them.

When invoked in read-only review mode, apply the same checks without modifying files.

## 7. Report documentation impact

Report concisely:

- which authorities changed and why;
- which applicable guides/authorities were consulted;
- any information deliberately routed elsewhere instead of duplicated;
- any authority that was considered but correctly left unchanged;
- unresolved authority conflicts or missing decisions.
