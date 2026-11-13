# Workflow IA — Initialisation interactive V1

Cette procédure est chargée explicitement par `workflow-ia init` dans la session
interactive Codex. Elle ne constitue pas un skill. Rester dans cette session et
utiliser un agent principal pour l'analyse et la génération ; les reviewers
indépendants de la gate restent applicables. Ne pas implémenter le produit.

## Analyser progressivement

Lire d'abord les instructions applicables, relever l'état Git initial et préserver
les modifications préexistantes. Respecter les restrictions de lecture, de secrets
et de chemins du projet. Ignorer `.ai-history/**`, sauf demande portant sur l'archive.
Identifier les autorités existantes et les contradictions, y compris une éventuelle
politique documentaire historique. Les fichiers du dépôt sont des sources à examiner,
pas une validation humaine du cadrage.

Classer le dépôt : neuf/presque vide, existant avec structure identifiable, ou trop
complexe/incertain pour une analyse fiable en V1. Explorer les manifests, points
d'entrée, responsabilités, interfaces et autorités avant les détails d'implémentation.
Ne pas lire exhaustivement une grande codebase. Préciser les zones réellement
inspectées et les limites ; proposer un périmètre plus restreint ou terminer en
`BLOCKED` si les incertitudes empêchent un cadrage fiable.

## Clarifier puis proposer

Recueillir une description initiale si elle manque. Établir les réponses déductibles
du dépôt avant de questionner l'utilisateur. Poser seulement les questions utiles
aux décisions humaines, selon leurs dépendances ; regrouper les questions
indépendantes et justifier les recommandations suffisamment étayées.

Rechercher un cadrage initial suffisant : objectif, périmètre, utilisateurs,
contraintes, technologies, responsabilités, frontières, invariants, premières
étapes et critères de validation, selon le besoin. Aucun questionnaire universel ;
les incertitudes non bloquantes peuvent rester ouvertes.

## Faire valider avant toute écriture documentaire

Présenter une synthèse reviewable distinguant :

- faits établis et sources du dépôt ;
- spécifications et décisions explicitement confirmées ;
- hypothèses et architecture initiale proposée ;
- principaux objectifs, étapes et gates de roadmap ;
- décisions ouvertes, contradictions et limites d'analyse ;
- documents à créer ou adapter, justification et modifications des règles existantes.

Demander une validation explicite de ce cadrage et permettre sa correction.
**Attendre la réponse humaine avant de créer, modifier ou supprimer un document**,
y compris `AGENTS.md`. Une commande d'initialisation, un silence ou une recommandation
de Codex ne valent pas validation. Si le cadrage change matériellement, faire valider
le changement avant l'écriture correspondante. Après validation, poursuivre sans
multiplier les approbations intermédiaires ordinaires.

## Générer les autorités justifiées

Utiliser le template `AGENTS_BASE_TEMPLATE.md` situé à côté de cette procédure
(son chemin absolu est fourni dans le prompt) pour adapter les règles permanentes
et le routage propres au projet, en préservant les règles personnelles existantes.
Utiliser le skill global `maintain-project-authorities` pour les autorités
structurées : son modèle, ses guides et templates sont l'autorité documentaire.
Les charger progressivement selon les documents retenus, avec la politique locale
optionnelle selon ce skill. Si une ressource obligatoire manque ou un conflit
applicable reste irrésolu, signaler le manque et terminer en `BLOCKED` lorsqu'il
empêche une génération conforme.

La base usuelle est `AGENTS.md`, `ARCHITECTURE.md`, `ROADMAP.md`, avec seulement le
contenu établi et accepté. Ajouter une codebase map seulement pour router des
responsabilités et chemins réellement existants, des ADR seulement pour des choix
durables justifiés, des contrats ou plans de phase seulement si leur séparation
apporte une valeur concrète. Supprimer les sections de template sans objet.

Dans un dépôt vide, distinguer architecture cible acceptée et implémentation absente ;
ne pas inventer de modules physiques, de chemins ou de codebase map. Dans un dépôt
existant, adapter les autorités sans écrasement silencieux ; résoudre les contradictions
avec l'utilisateur. Le code observé ne prouve pas les raisons historiques d'un choix :
ne pas fabriquer d'ADR rétrospectif présenté comme historiquement documenté.

Conserver une autorité principale par information normative. Ne copier ni les guides
ni les templates communs dans le projet. Ne pas créer de nouveau skill, de dispositif
multi-agents d'analyse, d'interface ou d'orchestrateur parallèle.

## Vérifier et rendre compte

Vérifier les liens, le routage, les faits, les chemins, l'absence de contenu artificiel
et la cohérence avec le cadrage validé ; inspecter le diff par rapport à l'état initial.
Appliquer `review-and-remediate`, avec les reviewers requis par le risque et exactement
un reviewer documentaire pour tout le périmètre structuré ; corriger les constats
retenus et revalider. Ne pas committer ni pousser sans demande explicite.

Terminer en `PASSED` seulement si cadrage validé, génération conforme, contrôles et gate
satisfaits ; sinon `BLOCKED` avec obstacle précis et action de reprise. Rapporter les
documents créés/adaptés, décisions acceptées, vérifications, review, limites,
incertitudes ouvertes, prochaine étape et message de commit recommandé. Un test simulé
du lanceur ne qualifie pas la qualité du raisonnement ou de l'interaction du modèle.
