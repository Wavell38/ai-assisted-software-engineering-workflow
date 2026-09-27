# Workflow d’ingénierie logicielle assistée par IA

Ce dépôt contient un workflow évolutif pour structurer le développement logiciel réalisé avec des assistants et agents IA.

Il s’est construit progressivement au fil de plusieurs projets et de l’évolution des capacités des modèles : d’une utilisation initialement centrée sur l’analyse, la compréhension et l’assistance ponctuelle au développement vers des tâches d’ingénierie de plus en plus autonomes, nécessitant davantage de cadrage, de contexte, de validation et de review.

L’objectif n’est pas de multiplier les documents, les agents ou les étapes de processus. Il est de fournir **juste assez de structure pour déléguer davantage sans perdre la maîtrise du périmètre, de l’architecture, des décisions et des preuves de validation**.

Ce dépôt représente l’état actuel de cette pratique. Il est amené à évoluer continuellement.

## Positionnement : Spec-Driven Development

Le workflow s’inscrit dans une logique de **Spec-Driven Development (SDD)** au sens large : expliciter le **quoi**, les contraintes et les critères d’acceptation avant de déléguer le **comment** de l’implémentation.

Il ne repose pas nécessairement sur un unique fichier de spécification. Sur un projet existant, la spécification utile peut être répartie entre plusieurs autorités : roadmap, architecture, ADR, contrats, plans de phase et tranche courante.

Le workflow va au-delà d’une simple séquence spécification → implémentation en ajoutant notamment :

- des autorités vivantes et séparées par responsabilité ;
- un chargement progressif du contexte ;
- des contrats et invariants explicites ;
- une validation proportionnée au risque ;
- une review indépendante adaptée au changement ;
- une boucle de remédiation ;
- une qualification à échelle représentative lorsque nécessaire ;
- un statut `BLOCKED` pour éviter d’inventer silencieusement une décision manquante ;
- un checkpoint anti-dérive lorsque les corrections locales commencent à remettre en cause la conception.

Il ne s’agit pas d’une implémentation de GitHub Spec Kit ou d’un autre framework SDD particulier. Le principe est utilisé comme base puis étendu selon les besoins rencontrés sur les projets.

## Principes

### Une autorité principale par information normative

Architecture, contrats, décisions, roadmap, règles d’exécution et preuves n’ont pas le même rôle.

Une information durable doit posséder une autorité principale identifiable plutôt que d’être recopiée dans plusieurs documents susceptibles de diverger.

### Autorités vivantes et archives

Les autorités vivantes (`ARCHITECTURE.md`, `CODEBASE_MAP.md`, contrats, roadmap, etc.)
décrivent l'état accepté courant : lorsqu'un fait change, l'état supersédé est remplacé au lieu
d'accumuler une chronologie de runs. Les ADR et rapports de qualification conservent au contraire
des décisions et preuves durables dans leur contexte.

Le skill opérationnel `maintain-project-authorities`, lorsqu'il est installé, applique cette
discipline avec le modèle documentaire et les guides du dépôt sans devenir lui-même une source
d'autorité.

### Chargement progressif du contexte

Un agent ne doit pas lire l’ensemble du dépôt et de sa documentation « au cas où ».

Le contexte est chargé progressivement à partir de la tâche courante, des règles applicables et des autorités réellement nécessaires.

### Séparation du raisonnement, de l’autorité et de l’exécution

Le workflow distingue :

- **l’état de raisonnement** : hypothèses, alternatives, discussion, découpage et arbitrages ;
- **l’état d’autorité** : connaissance durable et acceptée du projet conservée dans le dépôt ;
- **l’état d’exécution** : implémentation, validations, reviews, remédiations et rapports de run.

Une idée discutée ne devient pas automatiquement une décision du projet, et un rapport d’exécution ne devient pas automatiquement une autorité.

### Travail par tranches bornées

Le travail est découpé en tranches cohérentes disposant d’un objectif, d’un périmètre et de critères de validation compréhensibles.

Le découpage suit les responsabilités et les invariants en interaction plutôt qu’un nombre arbitraire de fichiers ou de lignes de code.

Le cadre reste volontairement flexible : un agent peut identifier qu’un dépassement du plan initial est nécessaire, mais celui-ci doit être rendu explicite et justifié plutôt que devenir une dérive silencieuse.

### Validation par les preuves

Des tests verts ne suffisent pas nécessairement à déclarer une tranche terminée.

Selon le projet et le risque, la validation peut inclure tests, analyse statique, build, mesures, qualification déterministe, comportement à échelle représentative, respect des contrats et cohérence architecturale.

### Review indépendante et proportionnée

L’implémentation et la review sont séparées.

L’agent principal sélectionne le plus petit ensemble de reviewers spécialisés nécessaire selon la nature du changement. Une tranche peut donc nécessiter plusieurs reviewers, un seul, ou aucun reviewer de code lorsqu’une review n’apporte pas de valeur.

Les dimensions disponibles comprennent notamment :

- conformité au contrat et au périmètre ;
- correctness comportementale ;
- qualité des tests et de la validation ;
- architecture, ownership et cohésion structurelle ;
- placement, routage et sémantique des autorités documentaires structurées.

Des analyses déterministes telles que SonarQube peuvent compléter ces reviews lorsqu’elles sont configurées, disponibles et pertinentes. Elles ne sont pas obligatoires par défaut.

### `BLOCKED` est un résultat valide

Un agent ne doit pas inventer une décision structurante uniquement pour terminer une tâche.

Une tranche peut se terminer explicitement en `BLOCKED` lorsqu’une décision manque, que des autorités se contredisent, qu’une preuve nécessaire ne peut pas être obtenue ou que la conception courante ne permet pas de satisfaire le contrat.

### Réévaluation avant accumulation des corrections

Des blockers répétés ou une complexité corrective croissante peuvent indiquer que le problème n’est plus local.

Le workflow prévoit alors un checkpoint anti-dérive visant notamment à poser la question :

> Le blocker doit-il être corrigé dans la conception actuelle, ou indique-t-il que la conception elle-même doit être réévaluée ?

L’investissement déjà réalisé n’est pas considéré comme une justification suffisante pour poursuivre une mauvaise direction.

### Complexité proportionnée au besoin

Tous les projets n’ont pas besoin de toutes les autorités, de tous les reviewers ou de tous les outils présents dans ce dépôt.

Un mécanisme supplémentaire doit résoudre un problème identifiable.

L’objectif est de conserver le workflow aussi simple que possible sans perdre la fiabilité nécessaire.

## Vue générale

```mermaid
flowchart TD
    A[Discussion / raisonnement] --> B[Spécification / autorités / tranche]
    B --> C[Prompt d'exécution borné]

    C --> D[Lecture progressive des autorités]
    D --> E[Implémentation]
    E --> F[Validation et preuves]

    F --> G[Classifier le changement]
    G --> H[Review indépendante adaptée<br/>si nécessaire]
    G --> I[Analyse déterministe<br/>si applicable]

    H --> J[Consolidation]
    I --> J

    J --> K{Constat matériel ?}
    K -->|Remédiable| L[Remédiation ciblée]
    L --> M[Revalidation / re-review ciblée]
    M --> J

    K -->|Aucun blocker| N[PASSED]
    K -->|Décision / preuve / conception bloquante| O[BLOCKED]

    N --> P[Rapport final]
    O --> P

    P --> Q[Réévaluation utilisateur + IA]
    Q --> R[Autorités / roadmap / tranche suivante]
    R --> S[Commit / point de rollback]
```

Le chemin exact dépend de la taille, du risque et de la nature du projet.

## Modèle documentaire

Le workflow définit plusieurs autorités possibles, sans imposer leur présence systématique.

| Autorité | Rôle |
| --- | --- |
| `AGENTS.md` | Règles permanentes applicables au travail des agents |
| `ARCHITECTURE.md` | Architecture actuellement acceptée |
| `CODEBASE_MAP.md` | Routage compact entre responsabilités, code et autorités |
| `adr/*` | Justification des décisions architecturales durables |
| `contracts/*` | Invariants, frontières et comportements normatifs actuels |
| `ROADMAP.md` | Trajectoire, état du projet, phases et gates |
| `phases/*` | Détail optionnel des phases complexes |
| `qualification/*` | Preuves, mesures et résultats de qualification |

Tous ces documents ne sont pas nécessaires sur un petit projet.

Le modèle complet est décrit dans [`DOCUMENTATION_MODEL.md`](DOCUMENTATION_MODEL.md).

## Convention d'intégration dans un projet

Le dépôt de workflow contient davantage de matériel que ce qu'un projet doit embarquer.

Dans un projet, le corpus de **politique documentaire** standard est copié sous
`docs/engineering/` et reste volontairement minimal :

```text
docs/
  engineering/
    DOCUMENTATION_MODEL.md
    adr/
      ADR_GUIDE.md
      ADR_TEMPLATE.md
    architecture/
      ARCHITECTURE_GUIDE.md
      ARCHITECTURE_TEMPLATE.md
      ARCHITECTURE_CHANGE_WORKFLOW.md
    codebase-map/
      CODEBASE_MAP_GUIDE.md
      CODEBASE_MAP_TEMPLATE.md
    contract/
      CONTRACT_GUIDE.md
      CONTRACT_TEMPLATE.md
    qualification/
      QUALIFICATION_GUIDE.md
      QUALIFICATION_REPORT_TEMPLATE.md
    roadmap/
      ROADMAP_GUIDE.md
      ROADMAP_TEMPLATE.md
      PHASE_PLAN_TEMPLATE.md
```

`AGENTS.md` reste à l'emplacement normal du projet et référence cette convention.

Les éléments suivants restent normalement dans le dépôt de workflow ou dans l'installation
globale de l'environnement agentique, et **n'ont pas besoin d'être copiés dans chaque projet** :

- `README.md` du workflow ;
- `ENGINEERING_WORKFLOW.md` ;
- le template `AGENTS_BASE_TEMPLATE.md` une fois le `AGENTS.md` projet créé ;
- les guides de génération de prompt et de sélection de modèle ;
- la politique et les fichiers opérationnels de review/remédiation ;
- `maintain-project-authorities`, `review-and-remediate` et les configurations de reviewers.

Cette séparation garde le contexte projet compact : l'agent dispose des autorités et politiques
documentaires nécessaires au projet, tandis que les procédures générales restent globales.

## Contenu du dépôt

### Workflow global

- [`ENGINEERING_WORKFLOW.md`](ENGINEERING_WORKFLOW.md) — processus complet : raisonnement, spécification, découpage, exécution, validation, review, remédiation, blockers, checkpoint anti-dérive, qualification, provenance et rollback.
- [`DOCUMENTATION_MODEL.md`](DOCUMENTATION_MODEL.md) — autorités documentaires, responsabilités et routage progressif du contexte.

### Base agent

- [`agent/AGENTS_BASE_TEMPLATE.md`](agent/AGENTS_BASE_TEMPLATE.md) — base de `AGENTS.md` à adapter à chaque projet.

### Maintenance des autorités projet

- [`skills/maintain-project-authorities/SKILL.md`](skills/maintain-project-authorities/SKILL.md) — procédure opérationnelle pour créer, modifier sémantiquement, revoir ou compacter les autorités structurées en appliquant `DOCUMENTATION_MODEL.md` et le guide du document concerné.

Le skill peut être installé globalement dans l'environnement agentique. Les projets n'ont pas
besoin d'en recopier le contenu lorsqu'il est déjà disponible globalement ; il applique le
corpus de politique documentaire du projet sous `docs/engineering/`.

### Review et remédiation

- [`review/REVIEW_AND_REMEDIATION_WORKFLOW.md`](review/REVIEW_AND_REMEDIATION_WORKFLOW.md) — politique générale de review indépendante et proportionnée.
- [`review/review-and-remediate/SKILL.md`](review/review-and-remediate/SKILL.md) — implémentation opérationnelle actuelle de la gate de review/remédiation.

Les configurations de reviewers sont regroupées avec ce skill :

- [`review/review-and-remediate/contract-reviewer.toml`](review/review-and-remediate/contract-reviewer.toml)
- [`review/review-and-remediate/correctness-reviewer.toml`](review/review-and-remediate/correctness-reviewer.toml)
- [`review/review-and-remediate/tests-reviewer.toml`](review/review-and-remediate/tests-reviewer.toml)
- [`review/review-and-remediate/architecture-reviewer.toml`](review/review-and-remediate/architecture-reviewer.toml)
- [`review/review-and-remediate/documentation-reviewer.toml`](review/review-and-remediate/documentation-reviewer.toml)

Leur emplacement dans ce dépôt sert à regrouper les éléments du workflow. Leur installation effective peut nécessiter de les placer ou de les adapter selon les conventions de l’outil agentique utilisé.

### Architecture

- [`architecture/ARCHITECTURE_GUIDE.md`](architecture/ARCHITECTURE_GUIDE.md)
- [`architecture/ARCHITECTURE_TEMPLATE.md`](architecture/ARCHITECTURE_TEMPLATE.md)
- [`architecture/ARCHITECTURE_CHANGE_WORKFLOW.md`](architecture/ARCHITECTURE_CHANGE_WORKFLOW.md)

### Cartographie du code

- [`codebase-map/CODEBASE_MAP_GUIDE.md`](codebase-map/CODEBASE_MAP_GUIDE.md)
- [`codebase-map/CODEBASE_MAP_TEMPLATE.md`](codebase-map/CODEBASE_MAP_TEMPLATE.md)

Le codebase map est conçu comme un **routeur de contexte**, pas comme une reproduction exhaustive de l’arborescence du dépôt.

### ADR

- [`adr/ADR_GUIDE.md`](adr/ADR_GUIDE.md)
- [`adr/ADR_TEMPLATE.md`](adr/ADR_TEMPLATE.md)

### Contrats

- [`contract/CONTRACT_GUIDE.md`](contract/CONTRACT_GUIDE.md)
- [`contract/CONTRACT_TEMPLATE.md`](contract/CONTRACT_TEMPLATE.md)

### Roadmap et phases

- [`roadmap/ROADMAP_GUIDE.md`](roadmap/ROADMAP_GUIDE.md)
- [`roadmap/ROADMAP_TEMPLATE.md`](roadmap/ROADMAP_TEMPLATE.md)
- [`roadmap/PHASE_PLAN_TEMPLATE.md`](roadmap/PHASE_PLAN_TEMPLATE.md)

### Qualification

- [`qualification/QUALIFICATION_GUIDE.md`](qualification/QUALIFICATION_GUIDE.md) — organisation des rapports, preuves, artefacts générés, scripts et fixtures de qualification.
- [`qualification/QUALIFICATION_REPORT_TEMPLATE.md`](qualification/QUALIFICATION_REPORT_TEMPLATE.md) — ossature compacte d'un rapport de qualification durable.

Les rapports de qualification restent dans la documentation. Les artefacts générés,
volumineux ou reproductibles restent séparés par défaut et ne sont promus dans le
versionnement que lorsqu'une preuve durable le justifie.

### Génération des prompts et sélection du modèle

- [`prompt/CODEX_PROMPT_GUIDE.md`](prompt/CODEX_PROMPT_GUIDE.md) — transformation du raisonnement et des autorités du projet en contrat d’exécution borné pour Codex.
- [`prompt/MODEL_REASONING_SELECTION_GUIDE.md`](prompt/MODEL_REASONING_SELECTION_GUIDE.md) — guide lu par ChatGPT pour recommander, avant chaque prompt, le modèle d’exécution et le niveau de raisonnement adaptés au coût cognitif réel de la tranche.

## Agnosticisme et implémentation actuelle

Les principes d’ingénierie, le modèle documentaire, le Spec-Driven Development, la gestion du contexte, les contrats, les gates et la séparation entre implémentation et review sont conçus pour rester largement indépendants d’un fournisseur ou d’un modèle particulier.

L’implémentation opérationnelle actuelle est toutefois principalement construite autour de **ChatGPT / OpenAI Codex** et contient donc des prompts, configurations de reviewers, modèles et mécanismes spécifiques à cet environnement.

Le workflow est donc **agnostique dans ses principes, mais pas entièrement dans son implémentation actuelle**.

Cette séparation est volontaire : les principes peuvent rester utiles tandis que l’outillage évolue.

## Utilisation

Ce dépôt n’est pas destiné à être copié intégralement dans chaque projet.

Il sert plutôt de base dans laquelle sélectionner les éléments nécessaires :

1. définir les règles permanentes utiles dans `AGENTS.md` ;
2. créer uniquement les autorités documentaires dont le projet a réellement besoin ;
3. expliciter suffisamment la spécification, les contrats et les critères d’acceptation avant l’implémentation ;
4. maintenir les autorités vivantes comme projections compactes de l’état accepté, avec `maintain-project-authorities` lorsqu’il est installé ;
5. découper le travail en tranches cohérentes ;
6. charger progressivement les autorités pertinentes ;
7. borner dans les prompts le delta documentaire attendu lorsqu’une tranche peut modifier une autorité ;
8. valider chaque tranche avec des preuves adaptées au risque ;
9. utiliser une review indépendante proportionnée au changement, incluant la review documentaire pour les autorités structurées ;
10. faire évoluer les autorités lorsque la vérité acceptée du projet change sans y recopier la provenance d’exécution.

Les mécanismes inutiles doivent rester absents.

## Outils associés

### [`prompts_archiver`](https://github.com/Wavell38/prompts_archiver)

Outil local utilisé en complément du workflow pour conserver une **provenance versionnée des runs Codex**.

Pour chaque tour finalisé dans un dépôt activé, il peut archiver sous `.ai-history/` :

- le prompt d’exécution exact (`prompt.md`) ;
- le rapport final produit par l’agent (`report.md`) ;
- un ensemble de métadonnées de run (`run.json`), notamment liées au contexte Git, au runtime et au cycle d’exécution.

L’objectif est de pouvoir relier plus facilement **ce qui a été demandé à l’agent, ce qu’il a rapporté et l’évolution effective du dépôt**, notamment autour des commits et points de rollback.

Ces archives constituent de la provenance et non une autorité du projet. Elles doivent être relues avant toute publication vers un dépôt public : les prompts, rapports ou métadonnées peuvent contenir des informations sensibles et l’outil n’effectue pas actuellement de détection ou de caviardage automatique.

## Langues

Les guides de ce dépôt sont principalement rédigés en français.

Les templates destinés à produire directement la documentation d’un projet sont en anglais par défaut.

Certaines configurations opérationnelles destinées aux agents sont également en anglais.

Cette convention peut évoluer indépendamment du workflow lui-même.

## Évolution

Ce dépôt doit être considéré comme une **photographie vivante d’une pratique d’ingénierie**, et non comme une méthode terminée.

Le workflow évolue en fonction :

- des problèmes réellement rencontrés sur les projets ;
- des mécanismes qui se révèlent utiles ou inutilement complexes ;
- de l’évolution des capacités de raisonnement et d’autonomie des modèles ;
- des nouveaux outils disponibles ;
- du retour obtenu sur les validations et les reviews.

Une règle ou une couche devenue inutile peut être supprimée aussi naturellement qu’une nouvelle peut être ajoutée.

L’objectif n’est pas de conserver le workflow actuel.

L’objectif est de conserver **le niveau de structure réellement nécessaire pour travailler de manière fiable avec les capacités disponibles à un instant donné**.
