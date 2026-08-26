# Engineering Guide

Ce dossier définit un standard léger pour construire et maintenir des projets pilotés avec ChatGPT/Codex.

L'objectif n'est pas de multiplier la documentation, mais de rendre explicites :

- le rôle de chaque autorité documentaire ;
- le routage du contexte vers les seules sources pertinentes ;
- la séparation entre architecture, décisions, contrats, trajectoire et preuves ;
- les conventions minimales permettant aux agents et aux relecteurs humains de se repérer rapidement.

## Principes directeurs

1. **Une information normative possède une autorité principale unique.** Les autres documents la référencent au lieu de la recopier.
2. **La documentation est écrite pour être relue efficacement par des humains et des agents.** Précision et densité priment sur la prose.
3. **Les templates sont des ossatures souples.** Une section sans information utile doit être supprimée.
4. **Le contexte est chargé progressivement.** Un agent ne doit pas parcourir tout le dépôt ou toute la documentation sans nécessité.
5. **La structure physique du code et la structure architecturale sont liées mais distinctes.** Un sous-dossier n'est pas automatiquement un sous-module architectural.
6. **Les décisions durables et les contrats vivants restent séparés conceptuellement.** Ils peuvent rester dans un même document lorsqu'ils sont très petits, mais ne doivent pas être confondus.

## Fichiers

### Modèle documentaire

- `DOCUMENTATION_MODEL.md` — rôles, autorités, anti-redondance et routage du contexte.

### Base agents et prompts

- `AGENTS_BASE_TEMPLATE.md` — base concise à adapter dans chaque dépôt.
- `RULES_FORMAT_PROMPTS.md` — guide de génération des prompts Codex.

### Architecture

- `ARCHITECTURE_GUIDE.md` — politique de construction et maintenance de `ARCHITECTURE.md`.
- `ARCHITECTURE_TEMPLATE.md` — template anglais minimal.
- `CODEBASE_MAP_GUIDE.md` — politique du graphe/module map.
- `CODEBASE_MAP_TEMPLATE.md` — template anglais minimal.
- `ARCHITECTURE_WORKFLOW.md` — processus de décision lorsqu'un changement touche l'architecture.

### Décisions et contrats

- `ADR_GUIDE.md` — politique des ADR.
- `ADR_TEMPLATE.md` — template anglais concis.
- `CONTRACT_GUIDE.md` — politique des contrats normatifs.
- `CONTRACT_TEMPLATE.md` — template anglais concis.

### Roadmap et exécution

- `ROADMAP_GUIDE.md` — rôle de la roadmap, statuts, phases et documentation de phase optionnelle.
- `ROADMAP_TEMPLATE.md` — template anglais minimal.
- `PHASE_DETAIL_TEMPLATE.md` — template anglais optionnel uniquement pour les phases qui nécessitent un détail séparé.
- `REVIEW_AND_REMEDIATION_WORKFLOW.md` — workflow de revue indépendante, consolidation et remédiation.

## Langues

Les guides de ce dossier sont en français. Les templates destinés à produire la documentation d'un dépôt sont en anglais par défaut.
