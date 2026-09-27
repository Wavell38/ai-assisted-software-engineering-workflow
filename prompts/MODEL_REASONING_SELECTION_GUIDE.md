# Guide de sélection du modèle et du niveau de raisonnement

## Rôle

Ce document guide **ChatGPT lorsqu'il prépare une tranche et génère son prompt d'exécution**.

Il sert à recommander, avant le run :

- le **modèle d'exécution** adapté au coût cognitif de la tranche ;
- le **niveau d'effort de raisonnement** associé ;
- la nécessité éventuelle de mieux spécifier ou découper la tranche avant exécution.

La sélection est effectuée par ChatGPT **avant de rendre le prompt**. Elle accompagne le prompt afin
que la configuration appropriée puisse être choisie dès le début du run ; elle ne fait pas partie
du contrat d'exécution lui-même.

Il s'agit d'un **guide de processus**, pas d'une autorité du projet.

Le choix doit être fondé sur le **coût cognitif réel de la tranche**, et non sur le nombre brut de
fichiers, de lignes de code ou la simple importance apparente de la tâche.

Les modèles, niveaux disponibles et coûts évoluent. La calibration ci-dessous reflète la famille
GPT-6 utilisée dans le workflow en septembre 2026. Vérifier l'offre courante lorsqu'une décision
dépend matériellement du coût ou de la disponibilité.

## Principe central

Évaluer séparément :

1. **la capacité de modèle nécessaire** ;
2. **la profondeur de raisonnement nécessaire** ;
3. **la qualité de la spécification et du découpage**.

La capacité du modèle et l'effort de raisonnement sont deux axes distincts.

Augmenter l'effort de raisonnement lorsque le problème est suffisamment bien cadré mais demande
davantage de profondeur.

Augmenter la capacité du modèle lorsque la difficulté vient surtout de l'ambiguïté résiduelle, de
la nouveauté du problème, de la reconstruction du cadre, de nombreux trade-offs plausibles ou d'un
couplage systémique qu'un raisonnement plus long ne suffit pas nécessairement à compenser.

Un modèle plus puissant ou un effort plus élevé ne doit pas compenser automatiquement une tranche
mal spécifiée ou mal délimitée.

Lorsque le travail peut être séparé en responsabilités cohérentes et indépendamment reviewables,
préférer la décomposition à l'escalade.

```text
travail difficile
      │
      ├── mal spécifié ou décomposable
      │       ↓
      │   clarifier / découper
      │
      └── cohérent et irréductible
              ↓
        difficulté de profondeur ?
          │             │
         oui           non
          │             │
          ▼             ▼
     augmenter       capacité de
     reasoning       modèle supérieure
```

Éviter le micro-découpage : une tranche doit rester suffisamment large pour produire un incrément
utile et conserver ses invariants réellement couplés.

## Évaluation du coût cognitif

Prendre notamment en compte :

- largeur du contexte nécessaire ;
- nombre de responsabilités ou modules concernés ;
- couplage sémantique entre ces responsabilités ;
- nombre d'invariants qui interagissent ;
- présence de contrats ou frontières multiples ;
- impact architectural ;
- degré d'ambiguïté résiduelle ;
- quantité de raisonnement nouveau nécessaire ;
- nécessité de construire ou reconstruire le cadre du problème ;
- nombre d'alternatives ou d'hypothèses plausibles à départager ;
- difficulté de validation ;
- concurrence, ordering, atomicité ou gestion d'état ;
- conséquences d'une erreur silencieuse ;
- difficulté du diagnostic lorsque la cause n'est pas connue ;
- caractère local ou systémique du problème.

Le volume de code est un signal secondaire.

# Sélection du modèle

## Sol — modèle principal

Utiliser **GPT-6 Sol** comme modèle d'exécution principal du workflow.

Sol couvre la quasi-totalité des tranches, depuis un travail très borné jusqu'à une exécution
cognitivement très exigeante, en modulant l'effort de `medium` à `max`.

Il est adapté notamment lorsque :

- la responsabilité de la tranche peut être définie clairement ;
- l'architecture cible est connue ou suffisamment orientée ;
- les autorités et invariants applicables peuvent être identifiés ;
- le problème peut être raisonné dans un cadre relativement stable ;
- la difficulté vient surtout de la profondeur, du nombre d'interactions ou du niveau de
  vérification nécessaire.

L'ancien domaine de travail couvert par Terra est absorbé par **Sol medium / high**.

Les tâches auparavant réservées à Sol restent principalement couvertes par
**Sol high / xhigh / max**.

## Astra — escalade de capacité

Utiliser **GPT-6 Astra** de manière exceptionnelle, lorsque la difficulté ne vient plus seulement
de la profondeur du raisonnement mais de la **capacité nécessaire pour construire correctement la
solution ou même le cadre du problème**, ou lorsque subsiste un doute matériel sur la capacité de
**Sol max** à résoudre le problème de façon suffisamment fiable.

Signaux typiques :

- architecture réellement indécise entre plusieurs solutions raisonnables ;
- problème nouveau ou fortement ambigu dont la bonne décomposition n'est pas encore connue ;
- reconstruction d'une intention ou d'un système à partir d'informations partielles,
  contradictoires ou distribuées ;
- diagnostic systémique où plusieurs couches peuvent produire le même symptôme ;
- plusieurs hypothèses globales restent plausibles après l'analyse locale ;
- redesign après accumulation de blockers ou de remédiations suggérant que la conception courante
  peut être mauvaise ;
- arbitrage transversal entre architecture, contrats, performance, validation et exploitation ;
- audit particulièrement large ou exigeant où de nombreuses conclusions localement plausibles
  peuvent être globalement incompatibles ;
- décision structurante difficile à vérifier a posteriori et coûteuse à inverser ;
- travail irréductible dont l'échec silencieux aurait un coût élevé et pour lequel Sol présente
  encore une incertitude matérielle malgré un effort élevé.

Astra ne doit pas devenir le modèle par défaut de toute architecture, review ou tâche importante.

Avant de l'utiliser, vérifier :

1. qu'une meilleure spécification ne supprimerait pas l'ambiguïté ;
2. qu'une décomposition cohérente ne permettrait pas de traiter le problème avec Sol ;
3. que la difficulté relève réellement de la capacité du modèle et pas seulement d'un besoin de
   raisonnement plus long ;
4. que le gain de fiabilité attendu justifie son coût supplémentaire.

### Astra et niveau de raisonnement

Dans ce workflow, **Astra high** est le point de départ normal lorsqu'une escalade exceptionnelle
vers Astra est justifiée.

Utiliser **Astra xhigh** lorsque le problème est à la fois fortement ambigu et profondément couplé,
par exemple pour un diagnostic systémique difficile, un redesign majeur ou une synthèse
transversale avec plusieurs hypothèses concurrentes.

Réserver **Astra max** aux problèmes exceptionnels et réellement irréductibles où la meilleure
capacité disponible et la profondeur maximale sont toutes deux justifiées.

Astra `low` et `medium` ne font pas partie de la calibration normale de ce workflow. Lorsque ce
niveau d'effort suffirait, rester sur Sol.

# Niveau de raisonnement avec Sol

## Medium

Utiliser **Sol medium** comme niveau minimal du workflow lorsque le raisonnement reste borné et que
la plupart des décisions sont déjà établies.

L'utiliser notamment pour :

- transformer des décisions déjà prises en prompt clair ;
- reformater ou densifier un prompt sans en modifier le contrat ;
- identifier les autorités directement applicables lorsque le routage est évident ;
- extraire les éléments matériels d'un rapport bien structuré ;
- vérifier une petite cohérence locale sans choix de conception ;
- préparer une tranche simple dont objectif, périmètre, invariants et validation sont déjà connus ;
- préparer un prompt de tranche bien spécifiée ;
- consolider quelques contraintes ou autorités sans conflit important ;
- choisir une découpe simple entre responsabilités déjà comprises ;
- interpréter un rapport dont les conséquences sont relativement directes ;
- traiter une intégration ou un changement non trivial mais conceptuellement établi ;
- décider entre quelques variantes locales dont les trade-offs sont connus.

Medium est le plancher volontaire du workflow. Ne pas descendre sous ce niveau pour économiser du
coût lorsque la tâche appartient à cette couche de cadrage.

## High

Utiliser **Sol high** comme **niveau par défaut** pour une tranche normale nécessitant un
raisonnement sérieux.

Il convient lorsque le travail mérite une analyse sérieuse même si aucune difficulté exceptionnelle
n'est présente, et devient particulièrement pertinent dès que plusieurs étapes, invariants ou
arbitrages interviennent.

Signaux typiques :

- plusieurs contrats ou invariants interagissent ;
- découpe de phase ou de tranche non évidente ;
- interprétation substantielle d'un rapport de qualification ou de review ;
- choix de conception dans une architecture globalement orientée ;
- frontière critique ou risque significatif d'erreur silencieuse ;
- analyse de concurrence, ordering, persistance ou état ;
- diagnostic non trivial mais dont le cadre reste suffisamment connu ;
- préparation d'un prompt complexe avec plusieurs critères de preuve et de blocage.

## Extra High / xhigh

Utiliser **Sol xhigh** lorsque le problème reste compatible avec Sol mais demande une profondeur de
raisonnement importante.

Signaux typiques :

- architecture complexe mais suffisamment orientée ;
- audit transversal fortement couplé ;
- diagnostic difficile avec plusieurs causes locales plausibles ;
- checkpoint anti-dérive ;
- raisonnement de scalabilité ou de performance susceptible d'affecter l'architecture ;
- nombreux invariants ou frontières dont les interactions doivent être vérifiées ensemble ;
- review critique d'un résultat susceptible de remettre en cause la prochaine tranche ;
- besoin important de contradiction, d'exploration d'alternatives ou de vérification globale.

## Max

Utiliser **Sol max** pour les problèmes les plus difficiles qui restent **bien cadrés et dans un
cadre conceptuel suffisamment établi**.

Exemples :

- interaction très dense de nombreux invariants connus ;
- diagnostic profond dont l'espace d'hypothèses est borné ;
- comparaison détaillée de plusieurs variantes d'une architecture déjà orientée ;
- vérification finale d'une décision structurante avant génération d'une tranche coûteuse ;
- problème où une erreur silencieuse aurait des conséquences importantes et où une profondeur
  maximale est justifiée.

`max` ne doit pas être choisi uniquement parce qu'une tâche est importante.

Si la difficulté principale devient la construction du cadre, l'ambiguïté fondamentale, la
nouveauté ou la présence de plusieurs architectures globalement plausibles, **préférer Astra**
plutôt que de considérer Sol max comme une escalade automatique suffisante.

# Combinaisons usuelles

| Type de travail ChatGPT | Modèle | Reasoning |
|---|---|---|
| Prompt quasi mécanique / décisions déjà établies | Sol | Medium |
| Cadrage quotidien / préparation normale d'un prompt | Sol | High |
| Découpe ou analyse substantielle | Sol | High |
| Plusieurs invariants / frontière critique / rapport complexe | Sol | High |
| Architecture complexe mais orientée | Sol | xhigh |
| Diagnostic transversal / checkpoint anti-dérive | Sol | xhigh |
| Problème extrêmement profond mais bien cadré | Sol | max |
| Audit particulièrement large ou exigeant | Astra | High ou xhigh |
| Architecture réellement ouverte / problème nouveau très ambigu | Astra | High |
| Diagnostic systémique / redesign majeur / forte ambiguïté globale | Astra | xhigh |
| Doute matériel sur la capacité de Sol max / problème exceptionnel et irréductible | Astra | xhigh ou max |

Cette table est une heuristique. Le coût cognitif réel, l'ambiguïté et la qualité du découpage
restent prioritaires. **Sol high est le choix par défaut**, Sol medium le plancher, et Astra reste
une escalade exceptionnelle.

# Sol max ou Astra ?

La décision ne doit pas être formulée comme une simple échelle de puissance.

Préférer **Sol max** lorsque :

- le problème est difficile mais déjà correctement formulé ;
- les autorités, invariants et critères de décision sont connus ;
- l'espace des solutions est suffisamment borné ;
- le besoin principal est davantage de profondeur et de vérification.

Préférer **Astra** lorsque :

- le cadre du problème lui-même doit être construit ou remis en cause ;
- plusieurs architectures ou explications globales restent raisonnables ;
- les preuves sont partielles, contradictoires ou très distribuées ;
- la difficulté vient de la nouveauté, de l'ambiguïté ou du couplage systémique ;
- une solution localement convaincante peut facilement être globalement fausse.

Ainsi, **Astra high peut être préférable à Sol max** pour certains problèmes conceptuellement
ouverts, tandis que **Sol max peut être préférable à Astra** pour un problème extrêmement profond
mais déjà bien défini.

# Règle de décomposition

Découper lorsqu'un travail combine plusieurs responsabilités qui peuvent être :

- spécifiées séparément ;
- raisonnées séparément ;
- implémentées séparément ;
- validées séparément ;
- reviewées séparément ;
- rollbackées séparément.

Une bonne décomposition suit les responsabilités et invariants, pas une cible arbitraire de taille.

Éviter cependant le micro-découpage : une tranche doit conserver un objectif unique, un périmètre
compréhensible, une validation propre et une review significative.

L'escalade de modèle ne doit pas servir à conserver artificiellement une tranche dont les
responsabilités sont naturellement séparables.

# Hors périmètre : reviewers

Cette calibration concerne le **modèle d'exécution de la tranche principale**.

Les reviewers indépendants sont gouvernés par leurs configurations propres et par le workflow de
review/remédiation. Ne pas dériver automatiquement leur modèle ou leur reasoning de cette grille,
et ne pas les modifier simplement parce que la calibration de l'exécuteur évolue.

# Décision avant génération du prompt

Avant chaque prompt, ChatGPT doit pouvoir répondre à :

1. Quelle est la responsabilité unique de la tranche ?
2. Quelles autorités et quels invariants interagissent ?
3. Quelle est l'ambiguïté résiduelle ?
4. Quel est le coût d'une erreur silencieuse ?
5. La tranche peut-elle être mieux spécifiée ou découpée sans perdre de cohérence ?
6. La difficulté vient-elle surtout d'un besoin de profondeur ou d'un besoin de capacité de modèle ?
7. Quel est le modèle minimal raisonnablement fiable ?
8. Quel niveau de raisonnement est suffisant ?
9. Sol à effort supérieur suffit-il, ou le problème justifie-t-il réellement Astra ?
10. L'escalade de modèle ou de reasoning compense-t-elle une mauvaise spécification ou décomposition ?

## Règle de sélection

La sélection est faite **avant** de rendre le prompt.

- **Sol medium** est le niveau minimal utilisé par ce workflow.
- **Sol high** est le choix standard par défaut.
- Utiliser `xhigh` ou `max` lorsque le coût cognitif le justifie.
- Lorsqu'il existe un doute raisonnable entre deux niveaux Sol adjacents, préférer le niveau
  supérieur plutôt que sous-dimensionner volontairement le run.
- Astra n'est pas l'étape automatique suivant Sol max. Il reste exceptionnel et doit être choisi
  lorsqu'un signal Astra est présent ou lorsqu'il existe un doute matériel sur la capacité de
  Sol max à traiter correctement la tranche.

Le but est d'utiliser la **configuration minimale raisonnablement fiable dans cette calibration**,
pas la configuration la moins coûteuse à tout prix.

## Sortie de sélection

Lorsqu'il rend un prompt d'exécution, ChatGPT affiche immédiatement **avant le prompt** la
configuration recommandée sous une forme compacte :

```text
Model: GPT-6 Sol
Reasoning: High
```

Adapter naturellement les valeurs (`Medium`, `High`, `xhigh`, `max`, ou Astra lorsqu'il est
justifié).

Ne pas ajouter de justification par défaut. Ajouter une raison courte uniquement lorsqu'elle aide
réellement à comprendre une escalade inhabituelle, une ambiguïté ou un choix Astra.

Cette sélection est une métadonnée de préparation : **ne pas la recopier dans le corps du prompt
Codex** sauf si l'outil d'exécution exige explicitement cette information.
