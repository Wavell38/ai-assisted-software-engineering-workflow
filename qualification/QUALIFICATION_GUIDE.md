# Guide des qualifications

## Rôle

Une qualification conserve une **preuve structurée** qu'un comportement, une
hypothèse, une performance, une intégration ou un gate a été évalué dans des
conditions définies.

Elle ne remplace ni :

- le contrat qui définit ce qui doit être vrai ;
- la roadmap qui conserve uniquement l'état synthétique ;
- le plan de phase qui définit le gate attendu ;
- les tests/scripts qui rendent la preuve reproductible.

Le rapport de qualification décrit les conditions, les résultats et leurs limites.
Les artefacts volumineux ou générés n'appartiennent pas par défaut dans la
documentation.

## Organisation recommandée

Préférer une organisation par phase ou domaine plutôt qu'un répertoire plat :

```text
docs/
  qualification/
    <phase-or-domain>/
      <qualification-id>.md
      <qualification-id>-manifest.json   # seulement si utile

artifacts/
  qualification/
    <phase-or-domain>/
      <qualification-id>/
        <generated evidence>
```

Les chemins exacts peuvent varier selon le projet, mais conserver la séparation
conceptuelle :

- **rapport durable** : documentation ;
- **preuve générée** : artefacts ;
- **outil reproductible** : code/tests/tooling ;
- **fixture durable nécessaire aux tests** : zone de test/fixture appropriée.

## Rapports

Un rapport Markdown doit rester centré sur ce qui est nécessaire pour interpréter la
preuve :

- objectif / question évaluée ;
- identité de la tranche, version ou baseline pertinente ;
- conditions et données réellement utilisées ;
- commandes ou procédure de reproduction ;
- résultats matériels ;
- critères de gate et verdict lorsqu'ils existent ;
- limites, incertitudes et portée de la conclusion ;
- liens ou identités des artefacts de preuve.

Éviter :

- les journaux bruts complets ;
- les longues chronologies d'exécution ;
- les copies de résultats déjà disponibles dans des fichiers machine ;
- la duplication du contrat ou du plan de phase.

## Artefacts générés

Les captures, images, vidéos, traces, dumps, exports, résultats intermédiaires, gros
JSON, assets expérimentaux et autres sorties générées ne doivent pas être placés
automatiquement sous `docs/qualification/`.

Par défaut :

1. les produire sous `artifacts/qualification/...` ou dans une zone temporaire
   explicitement dédiée ;
2. les exclure de Git lorsqu'ils sont reproductibles et n'ont pas de valeur durable ;
3. conserver dans le rapport leur identité, hash, paramètres ou commande de
   reproduction lorsque cela suffit ;
4. promouvoir explicitement seulement les artefacts dont la conservation versionnée
   est nécessaire à la preuve ou à une review future.

Un artefact promu doit avoir une raison identifiable d'être versionné.

## Scripts, tests et fixtures

Un script utilisé pour produire une qualification appartient avec le tooling ou le
code concerné, pas dans le dossier de documentation uniquement parce qu'il produit une
preuve.

Exemples :

```text
tools/qualification/
tests/
tests/fixtures/
<module>/tests/
```

Les fixtures nécessaires à des tests reproductibles doivent suivre la politique du
module/test correspondant. Les assets de test ne doivent pas être mélangés aux rapports
de qualification par commodité.

## Relation avec la phase

Le plan de phase définit **quelle preuve est requise**.

Le rapport de qualification conserve **la preuve obtenue et son interprétation**.

La roadmap conserve seulement **l'état synthétique du gate** et un lien lorsque
nécessaire.

```text
ROADMAP
   ↓ route vers
PHASE PLAN
   ↓ exige
QUALIFICATION REPORT
   ↓ référence
ARTIFACTS / TESTS / TOOLS
```

## Nommage

Préférer des identifiants stables et courts liés à la phase ou au gate.

Exemples :

```text
docs/qualification/Q0/mcp-smoke.md
docs/qualification/P3/performance-representative.md
artifacts/qualification/Q0/mcp-smoke/
```

Éviter d'encoder une longue phrase ou toute la chronologie dans le nom.

## Versionnement

Versionner par défaut :

- les rapports de qualification durables ;
- les petits manifests nécessaires à l'identité de la preuve ;
- les fixtures explicitement nécessaires aux tests ;
- les artefacts non reproductibles ou indispensables à une conclusion acceptée,
  lorsqu'une politique projet le demande.

Ne pas versionner par défaut :

- caches ;
- logs bruts reproductibles ;
- captures temporaires ;
- sorties intermédiaires ;
- artefacts volumineux générés uniquement pour inspection ponctuelle.

## Critère de qualité

Après lecture du rapport et de ses références, un reviewer doit pouvoir déterminer :

- ce qui a réellement été évalué ;
- dans quelles conditions ;
- quelle preuve existe ;
- si le gate est satisfait ;
- quelles limites empêchent d'étendre la conclusion au-delà de la preuve obtenue ;
- comment reproduire ou retrouver les artefacts utiles.
