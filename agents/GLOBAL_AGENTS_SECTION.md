<!-- workflow-ia:begin -->
## Shared Engineering Workflow

- Follow the applicable repository `AGENTS.md` and project authorities. Project-specific rules and decisions belong to their repositories.
- Use `maintain-project-authorities` to create, semantically update, review, or compact structured project authorities.
- Apply `review-and-remediate` after repository changes and initial validation, following its proportional review and remediation policy.
- Load only the skill references and project authorities relevant to the current task.

## Git

- Do not commit, tag, rewrite history, modify remotes, or perform Git remote operations or GitHub actions unless explicitly authorized.
- For each task that changes project files, include a concise recommended commit message in the final report.

## AI History

- Treat `.ai-history/**` as execution provenance, not project authority.
- Ignore its changes when evaluating the current-task Git diff or review scope, even when tracked by Git. Do not read, search, or modify it unless the task explicitly concerns AI history or archive maintenance.
<!-- workflow-ia:end -->