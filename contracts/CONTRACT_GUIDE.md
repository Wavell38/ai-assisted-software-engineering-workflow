# Guide des contrats

## Rôle

Un contrat est une autorité **normative et vivante**. Il répond à :

> Qu'est-ce qui doit être vrai actuellement à cette frontière, pour ce module ou pour ce comportement ?

Il doit être suffisamment précis pour guider l'implémentation, les tests et la review sans raconter l'historique de la décision.

## Quand créer un contrat dédié

Créer un fichier de contrat lorsque plusieurs tâches, modules ou reviewers ont besoin d'une définition stable d'un comportement, d'une interface ou d'invariants, notamment :

- ownership et frontières d'un module ;
- préconditions / postconditions ;
- ordering semantics ;
- identité, unités, précision ou déterminisme ;
- comportements d'échec ;
- interface entre composants ;
- règles métier critiques ;
- contraintes difficiles à reconstruire correctement depuis le code.

Ne pas créer un fichier séparé si le contrat tient réellement en quelques lignes et possède déjà une autorité naturelle unique.

## Relation avec les ADR

L'ADR conserve le **pourquoi** ; le contrat conserve le **quoi**.

Un contrat peut référencer les ADR qui justifient ses frontières. Il ne doit pas recopier leur rationale.

Lorsqu'un contrat évolue sans remettre en cause la décision architecturale, mettre à jour le contrat sans créer artificiellement un nouvel ADR. Lorsqu'une évolution modifie une décision durable, créer ou superseder l'ADR correspondant.

## Structure recommandée

Un contrat n'est pas un formulaire. Conserver uniquement les sections utiles :

1. purpose/scope ;
2. ownership/boundaries si pertinent ;
3. invariants ;
4. inputs/preconditions si pertinent ;
5. outputs/postconditions si pertinent ;
6. semantics particulières ;
7. failure behavior ;
8. validation references.

## Règles de rédaction

- Préférer des phrases normatives courtes et testables.
- Un invariant = une définition ; ne pas le reformuler dans plusieurs sections.
- Séparer les valeurs/identités/unités exactes des explications narratives.
- Ne pas prescrire une implémentation lorsque plusieurs implémentations peuvent satisfaire le contrat.
- N'inclure un détail d'implémentation que lorsqu'il constitue lui-même une contrainte contractuelle.
- Référencer les tests/qualifications sans recopier leurs résultats.
- Référencer les ADR sans recopier leur rationale.
- Supprimer toute section vide ou triviale.

## Contrats et code

Le contrat ne doit pas devenir une documentation parallèle exhaustive du code. Il documente ce qui serait coûteux ou dangereux à inférer : frontières, invariants, sémantiques, comportements observables et contraintes structurantes.

Si le code peut être modifié librement sans changer une propriété contractuelle, cette propriété n'a probablement pas besoin d'être décrite dans le contrat.

## Critère de qualité

Après lecture du contrat, un agent ou reviewer doit pouvoir déterminer sans ambiguïté :

- ce que le composant possède et ce qu'il ne possède pas ;
- les comportements obligatoires ;
- les invariants et cas limites importants ;
- les sémantiques exactes lorsqu'elles sont significatives ;
- les comportements interdits ou bloquants ;
- où trouver les preuves ou décisions associées.
