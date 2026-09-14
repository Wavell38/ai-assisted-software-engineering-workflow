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

## Ce qui n'y appartient pas

Le codebase map ne doit pas contenir :

- progression, statut ou historique de phases/tranches ;
- résultats détaillés de qualification ou de benchmark ;
- chronologie d'implémentation ou comptes rendus de runs ;
- inventaire exhaustif des fichiers, exemples, probes ou outils temporaires ;
- détails transitoires qui n'aident pas durablement à router une modification ou une lecture.

Un outil ou sous-module de qualification n'apparaît que s'il constitue lui-même une frontière
stable qu'il est utile de router indépendamment, pas parce qu'une phase l'a créé.

## Graphe et arborescence physique

Ne pas créer un nœud pour chaque sous-dossier.

Codex peut créer des sous-dossiers lorsqu'un groupe de fichiers forme une sous-responsabilité cohésive. Le codebase map ne change que si cette sous-responsabilité devient elle-même une frontière utile à comprendre ou router indépendamment.

À l'inverse, lorsqu'un nouveau module architectural est ajouté, son nœud doit être ajouté au graphe même si son implémentation initiale est petite.

## Profondeur

Ajouter un sous-module au graphe lorsqu'au moins une partie de la valeur suivante existe :

- ownership distinct ;
- contrat propre ;
- dépendances distinctes ;
- responsabilité stable et nommable ;
- besoin récurrent de charger ce sous-ensemble sans le reste du parent.

Ne pas ajouter de profondeur uniquement pour refléter une organisation esthétique du filesystem.

## Sémantique de l'état

`CODEBASE_MAP.md` est une autorité vivante de **routage actuel**, pas un journal append-only.

- `Owns` décrit les responsabilités stables possédées maintenant, pas les étapes qui ont permis
  de les construire ou qualifier.
- Remplacer les descriptions devenues obsolètes au lieu d'ajouter une nouvelle couche
  chronologique.
- Un identifiant de phase/tranche ne doit apparaître que s'il est réellement nécessaire pour
  identifier une autorité ou une frontière encore pertinente ; il ne sert pas à raconter
  l'historique du module.
- Lorsque le détail utile appartient à une architecture, un contrat, un plan de phase ou un
  rapport de qualification, conserver ici uniquement le routage vers cette autorité.

## Taille

Le graphe et les entrées doivent rester compacts. Si une entrée nécessite plusieurs paragraphes pour expliquer l'implémentation, vérifier d'abord que ce détail appartient réellement au codebase map et router vers une autorité spécialisée lorsque possible. Si la carte globale devient trop grande malgré cette discipline, conserver une vue globale et éventuellement des cartes locales uniquement pour les zones qui justifient réellement cette profondeur.

## Mise à jour

Mettre à jour `CODEBASE_MAP.md` lorsqu'une modification acceptée :

- ajoute/supprime un module ou sous-module architectural ;
- déplace sa responsabilité principale ;
- change ses dépendances majeures ;
- change son chemin principal ;
- ajoute/supprime une autorité contractuelle utile au routage.

Lors d'une mise à jour, retirer ou remplacer les informations de routage rendues obsolètes par le
nouvel état ; ne pas conserver leur chronologie dans la carte. Une phase ou qualification
terminée ne justifie pas à elle seule une mise à jour si aucune frontière stable de routage n'a
changé.

Une simple extraction de fichiers vers un sous-dossier interne ne nécessite généralement pas de mise à jour.
