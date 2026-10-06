# Workflow de changement architectural

## Objectif

Ce workflow décrit le traitement d'un changement susceptible d'affecter une frontière,
un ownership, une direction de dépendance ou une contrainte architecturale durable.

Il complète le workflow d'ingénierie global. Il ne remplace ni le run Codex standard,
ni sa validation, ni la gate de review/remédiation.

Il n'impose pas un ADR pour chaque changement : la première étape consiste précisément
à déterminer si l'autorité existante suffit.

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
    I -->|Yes| J[Create / supersede ADR]
    I -->|No| K[Record target state directly<br/>in the appropriate living authority]

    J --> L[Update affected living authorities:<br/>Architecture / Contract / Codebase Map]
    K --> L

    L --> G
    G --> M[Normal Codex run:<br/>implement + validate]
    M --> N[Review / remediation gate<br/>with architecture review when applicable]
    N --> O{Architecture and contracts<br/>respected?}
    O -->|No| P{Local remediation<br/>still fits accepted design?}
    P -->|Yes| R[Targeted remediation + revalidation]
    R --> N
    P -->|No| X[BLOCKED / final report]
    X --> Y[User + ChatGPT:<br/>reassess the design]
    Y --> B
    O -->|Yes| Q[Accept state]
    Q --> S[Update roadmap only if<br/>project state / plan changed]
```

## Règles

- L'ADR conserve le **pourquoi** d'une décision durable ; l'architecture, les contrats
  et le codebase map conservent l'état vivant correspondant.
- Lorsque le skill `maintain-project-authorities` est installé, l'utiliser pour appliquer les
  créations ou mises à jour sémantiques des autorités structurées concernées.
- Une décision structurante absente des autorités ne doit pas être inventée
  silencieusement pendant l'implémentation.
- Une extraction interne de fichiers ou de sous-dossiers n'est pas automatiquement un
  changement architectural.
- Lorsque l'état cible est déjà défini par les autorités applicables, ne pas créer un
  nouvel ADR uniquement parce que l'implémentation est importante.
- Lorsqu'une décision durable existante est remplacée, créer un nouvel ADR ou
  superseder explicitement l'ancien plutôt que de réécrire silencieusement l'historique.
- La review doit vérifier les frontières, ownerships, dépendances et contrats affectés,
  pas uniquement la correction locale du code.
- La gate de review/remédiation reste proportionnée au changement, mais un changement
  matériel d'architecture justifie normalement une review architecturale.
- Si l'implémentation ou la review montre que la décision acceptée n'est plus viable,
  revenir au raisonnement et aux autorités plutôt que d'empiler des remédiations locales.
- Mettre à jour `ROADMAP.md` seulement lorsque le changement modifie réellement l'état,
  le gate, la prochaine tranche, une dépendance ou la trajectoire du projet.
