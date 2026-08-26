# Guide du codebase map

## Rôle

`CODEBASE_MAP.md` est un **routeur de contexte**. Il aide un agent ou un humain à déterminer rapidement où se trouve une responsabilité et quelles autorités lire avant de modifier un module.

Il ne doit pas reproduire le filesystem complet ni devenir une seconde architecture détaillée.

## Un nœud représente quoi ?

Un nœud représente une frontière de compréhension suffisamment stable : module, sous-système ou sous-module lorsque celui-ci mérite d'être routé séparément.

Pour chaque nœud, conserver idéalement :

- nom ;
- chemin principal ;
- responsabilités possédées ;
- dépendances majeures ;
- dépendances interdites importantes ;
- liens vers contrat(s) et ADR pertinents.

## Graphe et arborescence physique

Ne pas créer un nœud pour chaque sous-dossier.

Codex peut créer des sous-dossiers lorsqu'un groupe de fichiers forme une sous-responsabilité cohésive. Le module map ne change que si cette sous-responsabilité devient elle-même une frontière utile à comprendre ou router indépendamment.

À l'inverse, lorsqu'un nouveau module architectural est ajouté, son nœud doit être ajouté au graphe même si son implémentation initiale est petite.

## Profondeur

Ajouter un sous-module au graphe lorsqu'au moins une partie de la valeur suivante existe :

- ownership distinct ;
- contrat propre ;
- dépendances distinctes ;
- responsabilité stable et nommable ;
- besoin récurrent de charger ce sous-ensemble sans le reste du parent.

Ne pas ajouter de profondeur uniquement pour refléter une organisation esthétique du filesystem.

## Taille

Le graphe doit rester compact. Si la carte globale devient trop grande, conserver une vue globale et éventuellement des cartes locales uniquement pour les zones qui justifient réellement cette profondeur.

## Mise à jour

Mettre à jour `CODEBASE_MAP.md` lorsqu'une modification acceptée :

- ajoute/supprime un module ou sous-module architectural ;
- déplace sa responsabilité principale ;
- change ses dépendances majeures ;
- change son chemin principal ;
- ajoute/supprime une autorité contractuelle utile au routage.

Une simple extraction de fichiers vers un sous-dossier interne ne nécessite généralement pas de mise à jour.
