# Guide des ADR

## Rôle

Un ADR conserve une **décision architecturale durable et sa justification**. Il répond principalement à :

> Pourquoi cette décision a-t-elle été prise, dans quel contexte, et avec quelles conséquences ?

Il n'est ni un journal de travail, ni une roadmap, ni un contrat complet.

## Quand créer un ADR

Créer un ADR lorsqu'une décision :

- modifie une frontière ou une direction de dépendance importante ;
- fixe un modèle architectural, un ownership ou une responsabilité durable ;
- introduit un choix technologique ou structurel dont le coût de changement est significatif ;
- tranche plusieurs alternatives raisonnables ;
- impose une contrainte que les futures implémentations doivent comprendre ;
- mérite de conserver le **pourquoi** indépendamment de l'état courant du code.

Ne pas créer d'ADR pour une décision locale évidente, un détail d'implémentation réversible ou une simple tâche de roadmap.

## Relation avec architecture et contrats

- `ARCHITECTURE.md` décrit **l'état architectural accepté**.
- l'ADR explique **pourquoi un choix durable existe**.
- un contrat décrit **ce qui doit être vrai actuellement**.

Après acceptation d'un ADR, mettre à jour les autorités vivantes affectées. Ne pas conserver dans l'ADR une copie détaillée du contrat si celui-ci possède sa propre autorité.

## Structure recommandée

Le template est volontairement court :

1. métadonnées ;
2. contexte ;
3. décision ;
4. rationale ;
5. conséquences ;
6. alternatives réellement pertinentes ;
7. liens vers les autorités affectées.

Toutes les sections sauf `Decision` et le contexte minimal peuvent être raccourcies ou supprimées si elles n'apportent rien.

## Règles de concision

- Une décision principale par ADR.
- Énoncer la décision normativement et une seule fois.
- Le contexte explique le problème, pas tout l'historique de la phase.
- La rationale conserve seulement les facteurs qui ont réellement déterminé le choix.
- Les alternatives rejetées tiennent idéalement en une ou deux phrases chacune.
- Les conséquences décrivent les effets durables, pas la liste des fichiers modifiés.
- Référencer architecture et contrats au lieu de les recopier.
- Éviter les longues sections génériques produites uniquement pour remplir le template.

## Statuts

Valeurs recommandées :

- `Proposed` — décision en discussion ;
- `Accepted` — décision autoritative ;
- `Superseded` — remplacée par un ADR ultérieur ;
- `Deprecated` — décision conservée pour l'historique mais plus applicable.

Ne pas réécrire silencieusement un ADR accepté pour changer sa décision historique. Créer un nouvel ADR lorsqu'une décision durable est remplacée, puis marquer l'ancien comme superseded.

## Critère de qualité

Un lecteur doit pouvoir comprendre rapidement :

- quel problème architectural existait ;
- ce qui a été décidé ;
- pourquoi ;
- quelles contraintes ou conséquences en résultent ;
- où trouver le contrat ou l'architecture vivante correspondante.
