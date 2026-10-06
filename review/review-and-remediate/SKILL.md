---
name: review-and-remediate
description: Proportionate review and remediation gate for repository-changing tasks. Use after implementation and initial validation, before any authorized commit and the final report. Isolate the current-task diff, select zero, one, or several reviewers according to material risk, and remediate verified findings. Small, bounded, low-risk changes can proceed without a reviewer; semantic structured-documentation changes require documentation review.
---

# Review and remediate

Apply this workflow after implementation and initial validation, before any authorized
commit and the final report. This is the reference procedure for reviewer selection,
context routing, review results, and remediation. It can also be read directly without
installing the skill.

## 1. Establish the review target

Use:

- the original user task as the implementation contract;
- the baseline HEAD and initial worktree state recorded before editing;
- only the changes produced by the current task;
- applicable AGENTS.md files, ADRs, architecture documents, contracts, and module guidance;
- initial validation results.

Do not provide reviewers with the implementer's reasoning, implementation narrative,
or provisional final report.

If the current-task boundary cannot be established without mixing unrelated changes,
stop the review and report the boundary problem.

Ignore `.ai-history/**` when determining implementation correctness.
An `.ai-history`-only diff does not require review.

## 2. Select review according to risk

Use zero, one, or several reviewers according to the actual change and the evidence
already available. Honor any independent review or validation explicitly required by
project authority. A small diff or successful tests alone do not establish low risk.

### When no reviewer is needed

Launch no reviewer for no effective diff, analysis-only work, `.ai-history`-only
changes, or ordinary prose/mechanical documentation corrections that change no
normative meaning.

A small local implementation or refactor can also proceed without a reviewer when
all of these conditions hold:

- the change covers one bounded responsibility and is straightforward to inspect;
- the expected behavior and acceptance criteria are already clear;
- it does not materially change architectural boundaries, shared ownership, public
  contracts, schemas, migrations, persistence, concurrency, security, identity,
  canonicalization, or safety-critical behavior;
- it does not semantically change a structured authority or an executable workflow rule;
- relevant checks or direct inspection establish the affected behavior and important
  edge cases; required validations have passed and no material uncertainty remains;
- no applicable authority requires independent review.

Record the reason and the supporting checks briefly in the final report. This is an
acceptance decision by the parent, not a reviewer `PASS`. Reassess the selection if the
scope grows, unexpected failures appear, or a material uncertainty emerges.

### When independent review is needed

For other changes, identify the material risks and choose the smallest set of
specialized reviewers that covers them. A single reviewer is sufficient when one
review dimension covers the risk; do not automatically pair contract and correctness
or add a tests reviewer for every behavioral change.

| Review dimension | Select when |
| --- | --- |
| `contract_reviewer` | Scope, exclusions, acceptance criteria, or normative/executable rules need independent verification. |
| `correctness_reviewer` | Changed behavior, state transitions, failure handling, or interactions carry material regression risk. |
| `tests_reviewer` | Coverage, assertions, fixtures, or the validity of the available proof need independent assessment. |
| `architecture_reviewer` | The change materially affects responsibility, ownership, dependencies, shared abstractions, or sensitive boundaries, as detailed below. |
| `documentation_reviewer` | The diff semantically changes one or more structured authorities, including workflow policy. |

Architecture review is required for substantial new production responsibilities,
material changes to module/package boundaries or shared abstractions, and changes
to public-contract, schema, migration, persistence, concurrency, security, identity,
or canonicalization semantics. Also select it when the change materially expands
mixed responsibilities or exposes a plausible decomposition problem in a touched
source unit. Merely touching a file in one of these areas, or its line count alone,
does not trigger architecture review.

Use exactly one documentation reviewer for the complete structured-documentation
scope, including mixed code/documentation tasks. Add another role only when the change
also presents a distinct contract, behavioral, validation, or architectural risk.

Give each selected reviewer a concrete review dimension. Launch multiple reviewers
in parallel, in fresh contexts independent of the implementation and of each other.

### Deterministic analysis

Use SonarQube project analysis when it is configured, usable, and relevant to the
changed implementation, or when project authority requires it. A minor change does
not by itself require a full-project analysis. When selected, analyze the current
worktree with the configured scanner and retrieve its quality gate and material
findings through the available integration. Never use stale results as current proof.

An unavailable or unsuccessful optional analysis does not block acceptance; report
the limitation. A project-required analysis remains required. Keep analysis findings
out of independent reviewer contexts and give them only to the parent for consolidation.
Wait for all requested reviews and analysis attempts to finish before consolidation.

## 3. Route context deliberately

Give `contract_reviewer`:

- the complete original implementation prompt;
- the target diff;
- referenced authority documents and acceptance criteria.

Give `correctness_reviewer`:

- the behavioral objective and material invariants;
- the target diff;
- access to all repository files needed to trace behavior.

Give `architecture_reviewer`:

- the target diff;
- applicable architectural authority, module boundaries, and shared abstractions;
- the touched source units and nearby abstractions needed to assess responsibility,
  cohesion, and decomposition;
- the original prompt only when needed to understand scope or ownership.

Give `tests_reviewer`:

- expected behavior and acceptance criteria;
- the production and test changes;
- relevant validation commands and test conventions.

Give `documentation_reviewer`:

- the complete structured-documentation diff for the current task;
- applicable `AGENTS.md`;
- repository access sufficient to inspect the changed authorities and their referenced sources.

The reviewer owns its own documentation-policy routing. When `maintain-project-authorities` is
installed, it must use that skill; otherwise it reads `docs/engineering/DOCUMENTATION_MODEL.md`
and the applicable project-copied type-specific guides directly. It must not assume the project
contains the workflow repository's prompt/review/agent-template material. Do not preload every
guide or launch one documentation reviewer per file.

All reviewers may inspect additional repository files when necessary.
The supplied references are starting points, not exploration boundaries.

## 4. Use stable reviewer configurations

Use the model and reasoning effort defined by each reviewer agent configuration.
Do not inherit, mirror, or downgrade the implementation agent's model or reasoning
effort merely because the implementation used a cheaper or lower-effort
configuration.

Override a reviewer configuration only when explicitly requested or when the
configured reviewer cannot complete the review adequately. Report any such override
and its reason in the final acceptance report.

Keep each selected review focused on its assigned risk, with enough context to
establish the facts.

## 5. Require structured review results

Each reviewer must return one structured review result containing:

- reviewer;
- verdict;
- review confidence;
- coverage and evidence: what was inspected and which checks or reasoning support the result;
- limitations: unverified behavior, unavailable checks, or uncertainty that affects confidence;
- findings.

Use exactly these verdicts:

- `PASS`: no material finding exists;
- `PASS_WITH_FINDINGS`: material findings exist, but none is critical or high severity;
- `FAIL`: at least one critical or high-severity finding exists.

Use `low`, `medium`, or `high` for overall review confidence.

Each finding must contain:

- stable identifier;
- reviewer;
- severity;
- confidence;
- file, symbol, or precise location;
- evidence;
- concrete impact;
- smallest defensible remediation.

Use these severity meanings consistently:

- `critical`: the implementation cannot be safely accepted because of a fundamental
  correctness, contract, architectural, security, data-integrity, or equivalent
  failure with potentially severe consequences;
- `high`: a material defect breaks or seriously endangers important required behavior,
  invariants, contracts, architecture, or validation and blocks acceptance until
  corrected or explicitly deferred by human decision;
- `medium`: a real, evidence-backed defect or gap with bounded impact that materially
  reduces correctness, confidence, maintainability, or required coverage;
- `low`: a minor but material issue with concrete impact.

Reject style-only observations unless they conceal a correctness, maintainability,
or contract risk.

A reviewer must explicitly report `no material findings` when appropriate, together
with the coverage and limitations of that conclusion. State when no material
limitation was identified; never imply that unperformed checks passed.

## 6. Disposition every finding

The parent must verify every finding against the repository before acting. Apply the
same disposition rules to material SonarQube findings when available; do not perform a
broad or risky refactor solely to satisfy a SonarQube rule or metric.

Classify each finding as exactly one of:

- accepted and corrected;
- accepted and deferred;
- rejected with factual evidence;
- human decision required.

An accepted finding is an implementation defect or gap, not an optional suggestion.
Correct it in the current task by default.

A finding against code or documentation created or materially changed by the current task is within
remediation scope when the correction is behavior-preserving, compatible with
repository authority, and requires no new product or architectural decision. The
original prompt need not have explicitly requested the quality correction.

For architecture findings, moving private implementation code, splitting a source
unit, or converting a module into a package/directory is ordinary remediation when
architecture and public contracts remain unchanged. When mixed responsibilities or a
defensible extraction boundary are confirmed, remediate to the smallest coherent
structure that resolves the finding.

Defer an accepted finding only when correcting it now would be unsafe, materially
broaden the task, or require a new product or architectural decision. Severity alone,
current functional correctness, or the convenience of a future slice are not
sufficient reasons. Record the exact reason in the final report; if a safely
correctable finding is intentionally left unresolved, classify it as
`human decision required` rather than self-approving the deferral.

Do not silently discard findings.

For a critical or high-severity correction, request targeted verification from
the originating reviewer or another independent reviewer.

Run the required validations after remediation. If SonarQube was used and analyzed
code changed, rerun it when available so the final signal reflects the remediated
worktree; an unavailable optional rerun remains non-blocking and must be reported.

## 7. Close the gate and report

Do not issue a provisional final report before review completes.

The parent accepts the result only when the task contract, applicable invariants,
required validations, and required reviews are satisfied. Verify every finding's
disposition and resolve material proof gaps or pending human decisions before
acceptance. Neither an absence of findings nor successful tests alone closes the gate.
Use the terminal status defined by the applicable workflow or task; reviewer verdicts
do not replace that status.

Add the review outcome to the task's final report, with detail proportional to the
change:

- reviewers selected and the risk each covered, or why none was needed;
- verdicts, confidence, supporting evidence, and material limitations;
- every finding's final disposition, with the correction, reason for deferral,
  factual rejection evidence, or decision needed;
- validations after remediation and independent verification when required;
- material analysis results and limitations, if analysis was requested;
- unresolved risks and their consequences for acceptance.

For a small change without findings, a brief rationale and the relevant validation
results are sufficient. Expand when findings, uncertainty, or a blocker need a
decision. Report configuration overrides when applicable; avoid raw logs, empty
sections, repeated chronologies, and duplicate descriptions.
