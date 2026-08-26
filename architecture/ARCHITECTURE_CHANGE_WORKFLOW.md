# Workflow de changement architectural

## Objectif

Ce workflow décrit le traitement d'un changement susceptible d'affecter une frontière, un ownership, une direction de dépendance ou une contrainte architecturale durable.

Il n'impose pas un ADR pour chaque changement : la première étape consiste précisément à déterminer si l'autorité existante suffit.

```mermaid
flowchart TD
    A[Need / proposed change] --> B[Assess architectural impact]

    B --> C{Changes a durable boundary,<br/>ownership, dependency direction<br/>or architectural constraint?}

    C -->|No| D[Use existing authorities<br/>and normal implementation workflow]
    C -->|Yes| E[Inspect Architecture, Codebase Map,<br/>related ADRs and contracts]

    E --> F{Existing authorities<br/>already define the target state?}
    F -->|Yes| G[Prepare bounded implementation tranche]
    F -->|No| H[Discuss and resolve the design]

    H --> I{Durable non-trivial<br/>decision worth preserving?}
    I -->|Yes| J[Create / update ADR decision]
    I -->|No| K[Record target state directly<br/>in the appropriate living authority]

    J --> L[Update living authorities:<br/>Architecture / Contract / Codebase Map]
    K --> L

    L --> G
    G --> M[Implement + validate]
    M --> N[Independent review]
    N --> O{Architecture and contract<br/>respected?}
    O -->|No| P[Remediate or reopen design]
    P --> B
    O -->|Yes| Q[Accept state and update roadmap]
```

## Règles

- L'ADR conserve la décision ; l'architecture et les contrats conservent l'état vivant.
- Une décision structurante absente des autorités ne doit pas être inventée silencieusement pendant l'implémentation.
- Une extraction interne de fichiers ou de sous-dossiers n'est pas automatiquement un changement architectural.
- La review doit vérifier le respect des frontières et contrats, pas uniquement la correction locale du code.
