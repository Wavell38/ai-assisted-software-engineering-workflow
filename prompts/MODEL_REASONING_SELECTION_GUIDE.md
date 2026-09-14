# Guide de sélection du modèle et du niveau de raisonnement

## Rôle

Ce document guide ChatGPT lors de la préparation d'une tranche Codex.

Il aide à choisir :

- le modèle d'exécution ;
- le niveau d'effort de raisonnement ;
- la nécessité éventuelle de découper la tranche avant exécution.

Il s'agit d'un **guide de processus**, pas d'une autorité du projet.

Le choix doit être fondé sur le **coût cognitif réel** de la tranche, et non sur le
nombre brut de fichiers ou de lignes de code.

Les modèles disponibles et leur tarification évoluent. La hiérarchie ci-dessous
reflète l'offre Codex disponible au 11 septembre 2026 ; vérifier la disponibilité et
le coût courant avant une décision sensible au budget.

## Principe central

Évaluer séparément :

1. **la capacité de modèle nécessaire** ;
2. **l'effort de raisonnement nécessaire** ;
3. **la qualité du découpage de la tranche**.

Un modèle plus puissant ou un effort plus élevé ne doit pas compenser automatiquement
une tranche mal délimitée.

Lorsque le travail peut être séparé en responsabilités cohérentes et indépendamment
reviewables, préférer la décomposition à l'escalade.

```text
tranche difficile
      │
      ├── décomposable
      │       ↓
      │   découper en tranches
      │   cohérentes
      │
      └── irréductible
              ↓
          augmenter modèle
          et/ou reasoning
```

Éviter le micro-découpage : une tranche doit rester suffisamment large pour produire
un incrément utile.

## Évaluation du coût cognitif

Prendre notamment en compte :

- largeur du contexte nécessaire ;
- nombre de responsabilités ou modules concernés ;
- couplage sémantique entre ces responsabilités ;
- nombre d'invariants qui interagissent ;
- présence de contrats ou frontières multiples ;
- impact architectural ;
- degré d'ambiguïté ;
- quantité de raisonnement nouveau nécessaire ;
- difficulté de validation ;
- concurrence, ordering, atomicité ou gestion d'état ;
- conséquences d'une erreur silencieuse ;
- difficulté du diagnostic lorsque la cause n'est pas connue.

Le volume de code est un signal secondaire.

# Sélection du modèle

## Luna

Utiliser **Luna** pour une tâche essentiellement mécanique, focalisée et très bornée.

Exemples typiques :

- modification locale évidente ;
- adaptation syntaxique ou configuration simple ;
- documentation bornée ;
- extraction, classification ou transformation répétitive ;
- petit script ;
- test simple dont le comportement attendu est déjà complètement défini.

Ne pas utiliser Luna lorsque la tâche exige de reconstruire une intention implicite,
d'arbitrer plusieurs contraintes ou de diagnostiquer une cause inconnue.

## Terra

Utiliser **Terra** pour le travail quotidien nécessitant un raisonnement réel mais dont
la conception est déjà suffisamment établie.

Exemples typiques :

- changement de code routinier mais non mécanique ;
- implémentation d'un composant dont le contrat est clair ;
- orchestration ou adaptateur borné ;
- tests substantiels ;
- refactorisation locale avec cible définie ;
- intégration entre quelques composants avec frontières connues.

Terra est le choix naturel lorsque le travail est bien spécifié et que le risque
conceptuel reste modéré.

## Sol

Utiliser **Sol** lorsque la tranche contient une difficulté conceptuelle importante ou
un risque élevé d'erreur silencieuse.

Signaux typiques :

- plusieurs contrats ou invariants qui interagissent ;
- diagnostic délicat ;
- frontière critique ;
- concurrence, ordering ou récupération d'état ;
- persistance/replay ;
- architecture déjà orientée mais intégration complexe ;
- audit transversal ;
- comportement métier ou technique à conséquence importante.

Sol est le modèle de référence lorsqu'il faut raisonner profondément sans que le
problème justifie encore le coût d'Astra.

## Astra

Utiliser **Astra** pour les problèmes les plus difficiles, notamment lorsque la
difficulté reste élevée après une bonne décomposition.

Signaux typiques :

- problème inconnu ou fortement ambigu nécessitant investigation et reconstruction ;
- bug difficile dont plusieurs explications restent plausibles ;
- choix architectural majeur entre plusieurs solutions raisonnables ;
- audit transversal très fortement couplé ;
- interactions de nombreux invariants où une solution localement plausible peut être
  globalement fausse ;
- tranche réellement irréductible dont l'échec serait coûteux.

Astra ne doit pas devenir le modèle par défaut de toute architecture ou de tout audit.
Avant de l'utiliser, vérifier explicitement :

1. qu'une meilleure spécification ne supprimerait pas l'ambiguïté ;
2. qu'une décomposition cohérente ne permettrait pas Sol ou Terra ;
3. que le gain de fiabilité attendu justifie le coût supplémentaire.

À titre indicatif seulement, le barème officiel Codex du 11 septembre 2026 facture
Astra matériellement plus cher que Sol. Ne pas figer ce ratio dans les décisions
durables : la tarification peut changer.

# Niveau de raisonnement

Le niveau de raisonnement est choisi indépendamment du modèle et selon les options
réellement exposées par le client Codex utilisé.

## Medium

Pour une tâche bornée dont le chemin de résolution est largement connu.

## High

Niveau standard pour une implémentation substantielle ou une analyse sérieuse.

## Extra High / xhigh

Pour les tranches où le risque vient principalement de la profondeur du raisonnement :

- diagnostic difficile ;
- interaction de plusieurs contrats ;
- ambiguïtés importantes ;
- audit transversal complexe ;
- correctness critique ;
- architecture partiellement établie.

## Maximum / niveau maximal disponible

Réserver le niveau maximal aux problèmes réellement irréductibles. Ne pas l'utiliser
pour compenser un mauvais découpage.

# Combinaisons usuelles

| Type de travail | Modèle | Reasoning |
|---|---|---|
| Modification mécanique / répétitive | Luna | Medium |
| Changement quotidien bien spécifié | Terra | Medium ou High |
| Implémentation substantielle déjà cadrée | Terra | High |
| Contrat / frontière critique | Sol | High |
| Diagnostic ou audit transversal délicat | Sol | Extra High |
| Architecture complexe mais suffisamment cadrée | Sol | Extra High |
| Problème très difficile / inconnu / irréductible | Astra | Extra High ou maximum disponible |
| Architecture réellement indécise avec nombreux trade-offs | Astra | maximum disponible |

Cette table est une heuristique. Le coût cognitif réel et la qualité du découpage
restent prioritaires.

# Règle de décomposition

Découper lorsqu'une tranche combine plusieurs responsabilités qui peuvent être :

- spécifiées séparément ;
- implémentées séparément ;
- validées séparément ;
- reviewées séparément ;
- rollbackées séparément.

Une bonne décomposition suit les responsabilités et invariants, pas une cible
arbitraire de taille.

Éviter cependant le micro-découpage : une tranche doit conserver un objectif unique,
un périmètre compréhensible, une validation propre et une review significative.

# Reviewers

Le niveau des reviewers doit correspondre à leur responsabilité propre, pas
automatiquement au modèle de l'exécuteur.

- **contract reviewer** : capacité suffisante pour comprendre le contrat principal ;
- **correctness reviewer** : généralement High ou plus selon le risque ;
- **architecture reviewer** : Extra High lorsque l'impact architectural est profond ;
- **tests reviewer** : High pour une validation substantielle ;
- reviewers spécialisés : calibrés selon leur risque et stabilisés entre runs
  comparables.

Un reviewer n'a pas besoin d'être systématiquement plus puissant que l'exécuteur.
Lorsque l'on compare des configurations d'exécuteur, garder les reviewers aussi stables
que possible.

# Décision avant génération du prompt

Avant chaque prompt Codex, ChatGPT doit pouvoir répondre à :

1. Quelle est la responsabilité unique de la tranche ?
2. Quelles autorités et quels invariants interagissent ?
3. Quelle est l'ambiguïté résiduelle ?
4. Quel est le coût d'une erreur silencieuse ?
5. La tranche peut-elle être découpée sans perdre de cohérence ?
6. Quel est le modèle minimal raisonnablement fiable ?
7. Quel niveau de raisonnement est suffisant ?
8. L'escalade de modèle compense-t-elle une mauvaise spécification ou décomposition ?

Le but est d'utiliser le niveau minimal raisonnablement fiable, pas la puissance
maximale disponible par défaut.
