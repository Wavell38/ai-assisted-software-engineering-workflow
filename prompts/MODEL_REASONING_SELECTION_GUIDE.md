# Guide de sélection du modèle et du niveau de raisonnement

## Rôle

Ce document guide ChatGPT lors de la préparation d’une tranche Codex.

Il aide à choisir :

- le modèle d’exécution ;
- le niveau d’effort de raisonnement ;
- la nécessité éventuelle de découper la tranche avant exécution.

Il s’agit d’un **guide de processus**, pas d’une autorité du projet.

Le choix doit être fondé sur le **coût cognitif réel** de la tranche, et non sur le nombre brut de fichiers ou de lignes de code.

---

## Principe central

Évaluer séparément :

1. **la capacité de modèle nécessaire** ;
2. **l’effort de raisonnement nécessaire** ;
3. **la qualité du découpage de la tranche**.

Un modèle plus puissant ou un effort plus élevé ne doit pas compenser automatiquement une tranche mal délimitée.

Lorsque le travail peut être séparé en responsabilités cohérentes et indépendamment reviewables, préférer la décomposition à l’escalade.

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

Éviter le micro-découpage : une tranche doit rester suffisamment large pour produire un incrément utile.

---

## Évaluation du coût cognitif

Prendre notamment en compte :

- largeur du contexte nécessaire ;
- nombre de responsabilités ou modules concernés ;
- couplage sémantique entre ces responsabilités ;
- nombre d’invariants qui interagissent ;
- présence de contrats ou frontières multiples ;
- impact architectural ;
- degré d’ambiguïté ;
- quantité de raisonnement nouveau nécessaire ;
- difficulté de validation ;
- concurrence, ordering, atomicité ou gestion d’état ;
- conséquences d’une erreur silencieuse ;
- difficulté du diagnostic lorsque la cause n’est pas connue.

Le volume de code est un signal secondaire.

---

# Sélection du modèle

## Luna

Utiliser **Luna** pour une tâche essentiellement mécanique et très bornée.

Exemples typiques :

- modification locale évidente ;
- adaptation syntaxique ou configuration simple ;
- documentation bornée ;
- petit script ;
- changement répétitif à faible ambiguïté ;
- test simple dont le comportement attendu est déjà complètement défini.

Caractéristiques :

- contexte faible ;
- peu d’invariants ;
- presque aucune décision de conception ;
- faible risque de mauvaise interprétation.

Ne pas utiliser Luna lorsque la tâche exige de reconstruire une intention implicite ou d’arbitrer plusieurs contraintes.

---

## Terra

Utiliser **Terra** pour une implémentation substantielle mais déjà suffisamment spécifiée.

Exemples typiques :

- implémentation d’un composant dont le contrat est clair ;
- orchestration ou adaptateur borné ;
- CLI ou tooling non trivial ;
- refactorisation locale dont la cible est déjà définie ;
- tests substantiels ;
- intégration entre quelques composants avec frontières connues.

Caractéristiques :

- raisonnement réel nécessaire ;
- contexte encore maîtrisable ;
- architecture et invariants principalement établis ;
- peu de décisions structurantes nouvelles.

Terra est le modèle naturel lorsqu’il faut **bien implémenter une conception déjà décidée**.

---

## Sol

Utiliser **Sol** lorsque la tranche contient une difficulté conceptuelle importante.

Signaux typiques :

- architecture ;
- ambiguïté significative ;
- plusieurs contrats ou invariants qui interagissent ;
- diagnostic difficile ;
- comportement économique ou métier à forte conséquence ;
- concurrence, atomicité, ordering ou récupération d’état ;
- persistance/replay ;
- frontière dont une mauvaise décision propagerait des erreurs ;
- audit transversal nécessitant de distinguer état réel, autorités et implications.

Caractéristiques :

- coût d’inférence élevé ;
- risque important d’erreur silencieuse ;
- besoin de raisonner au-delà d’une implémentation déjà complètement définie.

En cas d’hésitation réelle entre Terra et Sol lorsque l’erreur serait coûteuse, préférer Sol.

---

# Niveau de raisonnement

Le niveau de raisonnement est choisi indépendamment du modèle.

## Medium

Pour une tâche bornée dont le chemin de résolution est largement connu.

Utilisations typiques :

- tests/scripts/documentation simples ;
- vérification locale ;
- implémentation peu ambiguë ;
- modification mécanique mais non triviale.

Ne pas utiliser Medium lorsqu’il faut arbitrer plusieurs invariants subtils.

---

## High

Niveau standard pour une implémentation substantielle ou une analyse sérieuse.

Utilisations typiques :

- implémentation Terra non triviale ;
- architecture déjà décidée mais intégration complexe ;
- plusieurs modules avec frontières connues ;
- analyse de correctness ;
- conception limitée avec peu d’ambiguïtés résiduelles.

High doit suffire lorsque le problème est difficile mais bien cadré.

---

## Extra High

Pour les tranches où le risque vient principalement de la profondeur du raisonnement.

Utilisations typiques :

- diagnostic difficile dont la cause n’est pas connue ;
- interaction de plusieurs contrats ;
- ambiguïtés importantes ;
- audit transversal complexe ;
- correctness critique ;
- architecture partiellement établie nécessitant une analyse poussée ;
- problème où une solution localement plausible peut être globalement fausse.

Extra High ne doit pas être utilisé automatiquement sur toute tranche Sol.

---

## Max

Réserver **Max** aux problèmes réellement irréductibles ou aux décisions architecturales encore profondément indécises.

Utilisations typiques :

- choix architectural majeur entre plusieurs solutions raisonnables ;
- système avec de nombreux trade-offs non encore arbitrés ;
- problème très fortement couplé qu’une décomposition raisonnable ne simplifie pas.

Max n’est pas un substitut à une bonne décomposition.

Avant de choisir Max, vérifier explicitement qu’une séparation en tranches cohérentes ne réduirait pas suffisamment le coût cognitif.

---

# Combinaisons usuelles

| Type de travail | Modèle | Reasoning |
|---|---|---|
| Modification mécanique / très bornée | Luna | Medium |
| Tests, scripts ou documentation simples | Luna ou Terra | Medium |
| Implémentation substantielle déjà spécifiée | Terra | High |
| Orchestration / adaptateur borné | Terra | High |
| Refactorisation locale avec cible établie | Terra | High |
| Contrat ou frontière critique déjà décidée | Sol | High |
| Audit transversal / diagnostic délicat | Sol | Extra High |
| Architecture avec ambiguïtés importantes | Sol | Extra High |
| Architecture réellement indécise et irréductible | Sol | Max |

Cette table est une heuristique. Le coût cognitif réel de la tranche reste prioritaire.

---

# Règle de décomposition

Découper lorsqu’une tranche combine plusieurs responsabilités qui peuvent être :

- spécifiées séparément ;
- implémentées séparément ;
- validées séparément ;
- reviewées séparément ;
- rollbackées séparément.

Une bonne décomposition suit les **responsabilités et invariants**, pas une cible arbitraire de taille.

Exemple :

```text
mauvais découpage
- modifier fichiers A à D
- modifier fichiers E à H

meilleur découpage
- établir/implémenter la normalisation
- établir/implémenter le traitement L2
- établir/implémenter la matérialisation
```

Éviter cependant le micro-découpage.

Une tranche reste utile lorsqu’elle forme un incrément cohérent avec :

- un objectif unique ;
- un périmètre compréhensible ;
- une validation propre ;
- une review significative.

---

# Relation avec phases et roadmap

Une phase peut contenir plusieurs tranches de niveaux cognitifs différents.

Le découpage de roadmap ne doit donc pas être déterminé par le modèle choisi.

Ordre recommandé :

1. définir l’objectif de phase ;
2. identifier les responsabilités et gates ;
3. découper en tranches cohérentes ;
4. évaluer le coût cognitif de chaque tranche ;
5. choisir modèle + reasoning pour chaque tranche.

Si une tranche prévue devient trop complexe :

- la redécouper si les responsabilités peuvent être séparées ;
- sinon augmenter le modèle ou le reasoning ;
- si une décision structurante manque, revenir au niveau de raisonnement utilisateur + ChatGPT avant exécution.

---

# Audits

Un audit transversal ancien projet / architecture / contrats justifie généralement un modèle plus fort qu’une modification locale.

Pour un audit :

- préférer Sol lorsque plusieurs packages ou autorités doivent être croisés ;
- utiliser High si l’état est déjà bien connu et la vérification essentiellement factuelle ;
- utiliser Extra High lorsque l’audit doit reconstruire des responsabilités, distinguer documentation et implémentation, classifier des risques et proposer un découpage fiable.

Un audit ne doit pas être découpé artificiellement si la compréhension globale constitue précisément son objectif.

---

# Reviewers

Le niveau des reviewers doit être cohérent avec la difficulté de la tranche qu’ils évaluent.

Principes déjà retenus :

- **contract reviewer** : effort comparable à celui nécessaire pour comprendre le contrat principal ;
- **correctness reviewer** : généralement au moins High ;
- **architecture reviewer** : Extra High lorsque l’impact architectural est profond ;
- **tests reviewer** : High pour une validation substantielle, Medium seulement pour une vérification simple ;
- **documentation/exploration** : Medium lorsque le travail reste factuel et borné.

Les reviewers ne doivent pas être systématiquement plus puissants que l’exécuteur ; leur capacité doit correspondre à leur responsabilité propre.

---

# Décision avant génération du prompt

Avant chaque prompt Codex, ChatGPT doit pouvoir répondre à ces questions :

1. Quelle est la responsabilité unique de la tranche ?
2. Quelles autorités et quels invariants interagissent ?
3. Quelle est l’ambiguïté résiduelle ?
4. Quel est le coût d’une erreur silencieuse ?
5. La tranche peut-elle être découpée sans perdre de cohérence ?
6. Quel modèle est suffisant pour ce coût cognitif ?
7. Quel niveau de raisonnement est suffisant pour cette tranche ?
8. Le modèle ou reasoning choisi sert-il à compenser une mauvaise décomposition ?

Le choix final doit viser **le niveau minimal raisonnablement fiable**, pas la puissance maximale disponible par défaut.
