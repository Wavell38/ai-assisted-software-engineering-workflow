---
name: review-and-remediate
description: Final review and remediation gate for repository-changing tasks. Use after implementation and initial validation, before the final commit and final report. Isolate the current-task diff, select parallel reviewers, remediate safe findings, and enrich the final acceptance report. Skip code review for no-diff, analysis-only, or .ai-history-only work; classify documentation-only changes separately.
---

# Review and remediate

Apply this workflow after implementation and initial validation, before the final
commit and final report.

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

## 2. Classify the change

Use the smallest sufficient reviewer set:

- No effective diff, analysis-only work, or `.ai-history`-only changes:
  launch no reviewer.
- Documentation-only changes:
  launch no code reviewer unless the change alters an authoritative contract,
  architectural decision, or executable procedure.
- Small and local implementation or refactor:
  launch `contract_reviewer` and `correctness_reviewer`.
- Normal behavioral implementation:
  launch `contract_reviewer`, `correctness_reviewer`, and `tests_reviewer`.
- Also launch `architecture_reviewer` when the change:
  - creates substantial new hand-written production code, a new production module,
    or a new package;
  - introduces or materially expands several functions, classes, or components with
    potentially distinct responsibilities;
  - touches or materially enlarges an unusually large, tightly coupled, or
    multi-responsibility hand-written source unit;
  - materially changes ownership, dependency direction, module boundaries, or shared
    abstractions;
  - reveals a plausible decomposition boundary that warrants independent assessment.
- Transversal, architectural, public-contract, schema, migration, persistence,
  concurrency, security-sensitive, identity, or canonicalization work:
  also launch `architecture_reviewer`.

Do not select `architecture_reviewer` solely because generated files, vendored code,
declarative data, snapshots, or large fixtures have a high line count.

Launch the selected reviewers in parallel.

If the target includes hand-written implementation changes and a SonarQube project
scanner is configured and usable, run one full-project analysis of the same current
worktree in parallel. Use the configured scanner for project analysis and the available
SonarQube integration/MCP to retrieve its quality gate and material findings when
possible. SonarQube is optional: if unavailable or unsuccessful, continue normally and
report it as unavailable. Never use stale SonarQube results. Keep its findings out of
the independent reviewer contexts and give them only to the parent for consolidation.

Wait for all requested reviewer results and any successfully completed SonarQube
analysis before parent consolidation.

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

All reviewers may inspect additional repository files when necessary.
The supplied references are starting points, not exploration boundaries.

## 4. Use stable reviewer configurations

Treat the reviewers as an independent quality gate and as a calibration reference
for implementation quality.

Use the model and reasoning effort defined by each reviewer agent configuration.
Do not inherit, mirror, or downgrade the implementation agent's model or reasoning
effort merely because the implementation used a cheaper or lower-effort
configuration.

Keep reviewer model and reasoning configurations stable across comparable runs while
executor configurations are being evaluated.

Override a reviewer configuration only when explicitly requested or when the
configured reviewer cannot complete the review adequately. Report any such override
in the final acceptance report because it breaks direct calibration comparability.

Do not reduce review depth merely because implementation or initial validation
completed successfully.

## 5. Require structured review results

Each reviewer must return one structured review result containing:

- reviewer;
- verdict;
- review confidence;
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

A reviewer must explicitly report `no material findings` when appropriate.

Reviewers must not invent or calculate an overall numeric quality score.
Calibration metrics are calculated by the parent only after findings have been
verified and dispositioned.

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

A finding against code created or materially changed by the current task is within
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

## 7. Produce review calibration metrics

After the parent has verified and dispositioned the initial reviewer findings, record
the pre-remediation quality signal before corrections obscure the quality of the
original implementation.

Only accepted reviewer findings contribute to numeric scores. SonarQube findings are
tracked separately and never alter reviewer calibration scores:

- accepted and corrected findings count in the initial score;
- accepted and deferred findings count in the initial score;
- rejected findings do not count;
- findings requiring a human decision do not count numerically and must be reported
  separately.

For each selected reviewer, calculate:

`score = max(0, 100 - 100*critical - 25*high - 8*medium - 2*low)`

where each term is the number of accepted findings at that severity.

A reviewer with no accepted material finding receives `100`.

Also report the accepted finding counts by severity so the score never replaces the
underlying evidence.

Calculate the overall calibration score as the arithmetic mean of the selected
reviewer scores, rounded to the nearest whole number.

If no reviewer was required, report the review score as `N/A`.

The initial scorecard measures the quality of the implementation before remediation.
It is the primary signal for comparing executor model and reasoning configurations.

After remediation, validation, and any required targeted re-review, calculate the
same scorecard from residual accepted findings and report it as the final scorecard.

If a targeted re-review discovers a new accepted finding attributable to the
original implementation rather than to remediation, include it in the initial
scorecard as well.

Treat these scores only as internal comparative signals. They are not probabilities
or absolute measures of software quality. Compare them primarily across similar task
classes and reviewer sets.

## 8. Produce one final acceptance report

Do not issue a provisional final report before review completes.

The final report must remain detailed and task-specific. It is not a rigid form
and must contain enough information for a new session to understand the accepted
state and prepare the next task.

It must cover, when applicable:

- final status and delivered behavior;
- important implementation details and decisions;
- affected modules, contracts, and authority documents;
- meaningful deviations from the original plan;
- initial and final validation results;
- SonarQube status and, when available, its material results and dispositions;
- executor model and reasoning effort, when available;
- reviewers selected and why;
- reviewer model and reasoning configuration;
- each reviewer's verdict and review confidence;
- the initial review scorecard, including accepted finding counts by severity;
- the overall initial calibration score;
- every finding and its final disposition;
- corrections made because of review;
- rejected findings with evidence;
- human decisions required;
- the final review scorecard after remediation;
- the overall final calibration score;
- residual risks and deferrals;
- the recommended next step.

Avoid raw exploration logs, repeated chronologies, and duplicate descriptions.
Prefer decisions, evidence, final behavior, and remaining consequences.