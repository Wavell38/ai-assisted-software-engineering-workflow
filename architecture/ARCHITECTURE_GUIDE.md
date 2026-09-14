# Guide de l'architecture

## Rôle

`ARCHITECTURE.md` décrit **l'architecture actuellement acceptée** du système.

Il répond principalement à :

- quel modèle architectural est utilisé ?
- quelles sont les responsabilités et frontières majeures ?
- quelle est la direction des dépendances ?
- quels flux structurants traversent le système ?
- quelles contraintes transversales sont architecturales ?

Il ne doit pas devenir un historique des décisions : ce rôle appartient aux ADR.

`ARCHITECTURE.md` est une autorité vivante de l'état architectural accepté. Lorsqu'une structure
acceptée change, remplacer la description devenue obsolète et router le pourquoi durable vers un
ADR plutôt que d'accumuler la chronologie dans l'architecture.

## Contenu recommandé

Conserver uniquement les sections utiles au projet :

- architectural model ;
- system boundaries ;
- major modules / ownership ;
- dependency direction ;
- important data/control flows ;
- cross-cutting architectural constraints ;
- liens vers `CODEBASE_MAP.md`, ADR et contrats pertinents.

## Ce qui n'y appartient pas

- progression des phases ;
- TODO de roadmap ;
- compte rendu d'implémentation ;
- rationale longue d'une décision historique ;
- inventaire exhaustif des fichiers ;
- duplication détaillée des contrats.

## Niveau de détail

L'architecture doit être suffisante pour comprendre les frontières du système sans devoir ouvrir tous les modules, mais suffisamment compacte pour rester une autorité globale raisonnable à charger.

Lorsque la cartographie détaillée des modules devient volumineuse, déplacer le routage vers `CODEBASE_MAP.md` et conserver dans `ARCHITECTURE.md` uniquement la structure conceptuelle.

## Mise à jour

Mettre à jour l'architecture lorsqu'un changement accepté :

- ajoute/supprime une frontière architecturale ;
- déplace l'ownership d'une responsabilité ;
- modifie la direction des dépendances ;
- change le modèle architectural ;
- introduit un flux majeur ou une contrainte transversale durable.

Une simple réorganisation interne de fichiers ou de sous-dossiers ne nécessite pas une modification de `ARCHITECTURE.md` si les frontières architecturales restent identiques.

## ADR

Lorsqu'une modification architecturale résulte d'un choix durable et non trivial, conserver le **pourquoi** dans un ADR puis refléter uniquement l'état accepté dans `ARCHITECTURE.md`.

## Structure physique

La profondeur des dossiers doit suivre les sous-responsabilités cohésives du code, pas la profondeur du graphe architectural.

Un package peut contenir plusieurs sous-dossiers sans que chacun devienne un module architectural documenté.
