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

## Recommander le cadrage architectural

Pour un nouveau projet, identifier le modèle le plus approprié aux besoins et
contraintes établis. Présenter une recommandation par défaut avec les raisons
déterminantes, puis brièvement les alternatives réellement pertinentes et leurs
principaux compromis. Permettre à l'utilisateur d'accepter ou de modifier cette
proposition lors de la validation du cadrage ; ne pas lui demander systématiquement
de choisir un modèle technique abstrait lorsqu'une recommandation est suffisamment étayée.

Pour une application classique sans contrainte particulière de distribution, un
monolithe modulaire est souvent pertinent si plusieurs responsabilités stables sont
identifiées. Un petit utilitaire ou un projet peu complexe peut justifier une structure
plus simple. Cette préférence n'est ni universelle ni une exigence implicite : ROS 2,
embarqué, ECS, événementiel ou services distribués restent sélectionnables selon les besoins.

Pour un projet existant, identifier d'abord les contraintes, conventions, frontières
et responsabilités établies dans les autorités et le code. Préserver l'architecture
existante lorsqu'elle est acceptée et suffisamment identifiable. Toute migration ou
modification significative du modèle exige une proposition explicite, justifiée et
validée dans le cadrage ; ne jamais l'introduire silencieusement pendant l'initialisation.

Le cadrage architectural à valider doit préciser les responsabilités, frontières et
directions de dépendance importantes, au-delà du nom du modèle. Distinguer architecture
de déploiement, organisation interne du code et organisation des agents IA. Ne pas
imposer de couches, interfaces, packages, sous-agents ou `AGENTS.md` imbriqués sans
nécessité démontrée.

## Déterminer la langue documentaire

Distinguer la langue de communication avec l'utilisateur de la langue des autorités
documentaires du projet. La langue de la conversation ne détermine pas celle des
documents ; celle des guides et templates globaux non plus.

- Pour un dépôt neuf sans convention établie, demander la langue documentaire
  préférée en proposant **English** par défaut. Cette proposition ne vaut pas choix
  accepté sans réponse de l'utilisateur.
- Pour un dépôt existant, rechercher d'abord les conventions explicitement définies
  dans `AGENTS.md`, les autres autorités et la documentation pertinente. Si aucune
  règle explicite ne tranche, examiner la cohérence des usages documentaires existants.
- Lorsqu'une convention cohérente existe, la conserver ou la proposer dans le cadrage
  sans imposer de question supplémentaire. En l'absence de convention identifiable,
  demander la préférence en proposant **English** par défaut ; en cas d'ambiguïtés
  ou de conventions contradictoires, demander une clarification avant de générer.

Inclure la langue retenue et sa source dans le cadrage soumis à validation. Après
validation, la consigner explicitement dans le `AGENTS.md` du projet pour les futures
modifications documentaires, même si elle paraît déjà évidente. Appliquer cette langue
de façon cohérente au contenu rédigé dans `AGENTS.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
`CODEBASE_MAP.md`, les ADR, contrats et plans de phase retenus. Préserver les noms de
fichiers, chemins, identifiants techniques et liens utiles.

Les guides et templates globaux de Workflow IA conservent leur langue source ; adapter
le contenu final généré à la convention du projet. Ne pas traduire automatiquement
l'ensemble de la documentation d'un dépôt existant : une migration linguistique
globale exige une décision explicite et un périmètre distinct.

## Traiter la provenance facultative

Les règles globales relatives à `.ai-history/**` s'appliquent indépendamment de la
présence d'une archive, de l'installation de `prompts_archiver` et de son activation
effective pour ce dépôt. Ces quatre éléments sont distincts : une archive existante
ne prouve ni l'installation de l'outil ni son activation actuelle ; l'installation
ne prouve pas l'activation. Ne jamais supposer l'outil installé ou activé.

Par défaut, ne pas installer ni activer `prompts_archiver`, ne pas créer `.ai-history/`
et ne pas modifier `.gitignore` au seul motif que l'outil pourrait être utilisé.
Ne pas ajouter de règles redondantes dans le `AGENTS.md` projet lorsque les règles
globales suffisent. Ne pas modifier les autorités architecturales ou de planification
en fonction de l'utilisation de cet outil.

Ne pas introduire de question obligatoire sur cet outil si la réponse ne change pas
les documents à générer. Si son activation effective pour le dépôt est déterminée de
manière fiable par une configuration explicite accessible hors de l'archive, elle peut
être mentionnée dans le récapitulatif d'initialisation, avec sa source. Sinon, ne pas
déduire un état actif ou inactif ni chercher dans l'archive pour le déterminer.

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

Consigner la décision architecturale acceptée dans `ARCHITECTURE.md` et conserver sa
justification dans un ADR lorsqu'elle mérite une conservation durable, selon le guide ADR.
Pour le routage, `AGENTS.md` référence principalement les autorités générales et les
emplacements documentaires ; `ARCHITECTURE.md` référence les ADR pertinents pour ses
décisions ; `CODEBASE_MAP.md` référence les ADR ou contrats pertinents pour les
responsabilités qu'il route. Chaque ADR conserve sa décision et sa justification dans
son propre fichier. Éviter l'énumération systématique des ADR individuels dans `AGENTS.md` ;
un lien direct reste utile lorsqu'une décision transversale gouverne les travaux concernés.
Ne pas créer d'index ADR supplémentaire sans besoin concret.

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
