# Guide de la roadmap

## Rôle

`ROADMAP.md` est l'index compact de la **trajectoire du projet et de son état accepté**.

Elle doit permettre de répondre rapidement à :

- où en est le projet ?
- quelle phase ou tranche est active ?
- quels gates sont ouverts, passés ou bloqués ?
- quelles sont les prochaines étapes ?
- où se trouve le détail lorsqu'une phase en nécessite davantage ?

## Ce qui appartient dans la roadmap

- phases et sous-phases significatives ;
- statut courant ;
- gates et conditions de passage résumées ;
- dépendances majeures entre phases ;
- prochain objectif ou prochaine tranche ;
- liens vers documents de phase ou autorités spécialisées lorsque nécessaires.

## Ce qui n'y appartient pas

- architecture détaillée ;
- rationale complète d'une décision ;
- contrats complets ;
- journal chronologique de toutes les modifications ;
- résultats détaillés de tests, benchmarks ou qualifications ;
- listes détaillées de tranches lorsqu'un document de phase les possède déjà ;
- longs comptes rendus Codex ;
- duplication de contenu disponible dans une autorité spécialisée.

## Règle de compacité

La roadmap est un **index**, pas un résumé détaillé des documents qu'elle référence.

Lorsqu'une phase possède un document `Details` dédié, l'entrée correspondante dans
`ROADMAP.md` doit rester strictement synthétique. Ne pas y recopier :

- le scope détaillé ;
- la liste complète des tranches ;
- les décisions temporaires de phase ;
- les résultats de qualification ;
- l'historique d'implémentation ;
- les explications déjà disponibles dans le document de phase.

Par défaut, une phase tient en :

- identifiant + titre ;
- statut ;
- objectif en une ou deux lignes maximum ;
- gate/résultat important en une ligne lorsque utile ;
- dépendances majeures lorsque utiles ;
- lien `Details` lorsque le détail existe.

Si davantage d'explications sont nécessaires pour comprendre ou exécuter la phase,
créer ou enrichir le document de phase au lieu d'allonger la roadmap.

## Statuts

Utiliser un vocabulaire petit et stable. Exemple :

- `PLANNED`
- `IN PROGRESS`
- `BLOCKED`
- `DONE`
- `DEFERRED`

Un gate peut utiliser `OPEN`, `PASSED` ou `BLOCKED` si cette distinction est utile.

## Documents de phase optionnels

Ne pas créer systématiquement un fichier par phase.

Créer `phases/<id>.md` lorsqu'une phase :

- devient trop détaillée pour la roadmap ;
- contient plusieurs tranches dont le séquencement mérite d'être conservé ;
- possède un contexte, des contraintes ou des critères de qualification propres ;
- doit conserver un état local sans surcharger les autorités globales.

Le document de phase peut contenir :

- objectif et scope plus détaillés ;
- découpe en tranches ;
- références aux ADR/contrats/architecture ;
- critères de qualification spécifiques ;
- décisions temporaires nécessaires à la phase qui ne constituent pas une autorité durable.

Il ne doit pas recopier les autorités globales.

## Mise à jour

Mettre à jour la roadmap lorsqu'un changement accepté modifie réellement :

- le statut d'une phase ;
- le gate ;
- la prochaine tranche ou décision ;
- le découpage futur ;
- une dépendance de planification ;
- l'existence d'un document de phase pertinent.

Ne pas annoncer une phase comme `DONE` avant que les preuves/validations nécessaires aient été obtenues.

Une mise à jour de phase ne justifie pas de recopier son rapport ou ses preuves dans
la roadmap. Mettre à jour uniquement l'état et le routage nécessaires.

## Routage

La roadmap peut pointer vers les documents nécessaires mais ne doit pas forcer leur
lecture lorsqu'ils sont hors du périmètre de la tâche.

Une bonne entrée agit comme un routeur : elle indique **où regarder si le détail est
nécessaire**, sans intégrer ce détail elle-même.
