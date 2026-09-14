---
name: maintain-project-authorities
description: Operational procedure for creating, semantically updating, reviewing, or compacting structured project authorities in repositories using the standard `docs/engineering/` project documentation-policy layout. Use whenever a task may change ROADMAP.md, CODEBASE_MAP.md, ARCHITECTURE.md, phase plans, contracts, ADRs, qualification reports, or equivalent governed authorities, including small semantic updates.
---

# Maintain project authorities

Use this skill to apply the project's documentation model consistently. This skill is a
procedure, not a source of project truth: project authorities, `docs/engineering/DOCUMENTATION_MODEL.md`, and the applicable type-specific guides remain authoritative.

## 1. Establish the documentation scope

- Read the applicable `AGENTS.md` first.
- Identify every structured authority the task may create or change.
- Establish the current-task diff/baseline when maintaining existing documents.
- If no accepted project fact owned by a document changed, do not edit that document merely
  because implementation work occurred.

## 2. Load only the policy needed

The standard project documentation-policy root is `docs/engineering/`.

A project is only expected to copy the documentation-policy subset it needs there: the
documentation model plus the ADR, architecture, codebase-map, contract, qualification, and
roadmap guidance/templates. Do not expect the workflow repository's prompt, review,
agent-template, README, or global-skill material to exist in the project copy.

Load context progressively from `docs/engineering/`:

1. `docs/engineering/DOCUMENTATION_MODEL.md`;
2. the guide for each target document type;
3. the corresponding template only when creating a document, materially restructuring it,
   or when the guide explicitly requires it;
4. only the project authorities, code, phase state, or evidence needed to establish the facts
   being written.

Standard guide locations are:

- architecture -> `docs/engineering/architecture/ARCHITECTURE_GUIDE.md`
- codebase map -> `docs/engineering/codebase-map/CODEBASE_MAP_GUIDE.md`
- ADR -> `docs/engineering/adr/ADR_GUIDE.md`
- contract -> `docs/engineering/contract/CONTRACT_GUIDE.md`
- roadmap and phase plans -> `docs/engineering/roadmap/ROADMAP_GUIDE.md`
- qualification -> `docs/engineering/qualification/QUALIFICATION_GUIDE.md`

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

These examples do not override the guides under `docs/engineering/`.

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
