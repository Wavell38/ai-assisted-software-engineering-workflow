# Codex Prompt Generation Guide

## Rôle du guide

Ce guide s'adresse à ChatGPT lorsqu'il prépare un prompt Codex à partir de la
conversation courante et des sources du projet.

Il sert à conserver une ligne de génération stable entre les conversations et les
phases du projet. Il ne remplace ni les autorités du dépôt ni les décisions prises
pendant la discussion ; il encadre leur transformation en un contrat d'exécution
clair pour Codex.

Avant de rendre le prompt, sélectionner le modèle d'exécution et le niveau de raisonnement selon
`MODEL_REASONING_SELECTION_GUIDE.md`. Afficher cette recommandation immédiatement avant le prompt
selon le format défini par ce guide. La calibration des modèles et niveaux appartient uniquement
à ce document de sélection : ne pas la dupliquer ici.

## Instructions de génération

Pour chaque prompt Codex, privilégie une forte densité informationnelle sans sacrifier la précision.

Tiens compte des sources projet disponibles et à jour (`AGENTS.md`, architecture, roadmap, ADR/design docs, contrats et autres autorités pertinentes).

Lorsque la tranche peut créer ou modifier sémantiquement une autorité structurée, borne
explicitement le **delta documentaire** attendu. N'utilise pas une instruction générique du
type « update documentation as needed ». Indique seulement les autorités dont l'état peut
réellement changer et le type de changement attendu. Le delta documentaire peut explicitement
être `none`.

Lorsque le skill `maintain-project-authorities` est installé, demande à Codex de l'utiliser pour
toute création ou mise à jour sémantique d'une autorité structurée. Le corpus de politique
documentaire du projet vit sous `docs/engineering/` ; le skill applique
`docs/engineering/DOCUMENTATION_MODEL.md` et les guides projet correspondants, que le prompt ne
doit pas recopier.

Traite les décisions explicitement établies dans la conversation courante comme le
delta de conception à transcrire. Distingue une décision d'une hypothèse, d'une option,
d'un exemple ou d'une piste encore exploratoire. Ne transforme pas silencieusement une
possibilité discutée en exigence normative et n'affaiblis pas non plus une décision
explicitement arrêtée.

Les patterns et précédents existants du dépôt sont des indices de conception, pas des
autorités lorsqu'ils contredisent une règle explicite actuellement applicable dans
`AGENTS.md`, l'architecture, un ADR ou un contrat autoritatif. Ne reproduis pas une
convention historique uniquement parce qu'elle existe si une autorité plus récente
impose désormais une direction différente.

Si des sources pertinentes sont contradictoires, manifestement périmées ou
insuffisantes pour établir une décision nécessaire à la tranche, ne réconcilie pas
silencieusement le conflit par invention. Utilise la décision explicitement établie
dans la conversation lorsqu'elle tranche le point ; sinon, rends l'ambiguïté visible
au lieu de la convertir en contrainte arbitraire.

Le prompt doit principalement décrire le **delta propre à la tranche**. Ne répète pas une règle ou une décision déjà autoritative et directement récupérable dans les sources ; référence plutôt explicitement l'autorité pertinente lorsque Codex doit la consulter.

Conserve explicitement toute information dont la suppression obligerait Codex à inférer une décision propre à la tranche, notamment :

* frontières architecturales nouvelles ou spécifiques à la tranche ;
* invariants nouveaux ou spécifiques à la tranche ;
* valeurs et seuils ;
* ordering semantics ;
* cas limites ;
* exclusions importantes ;
* critères mesurables ;
* conditions de blocage ;
* critères d'acceptation.

Élimine les répétitions sémantiques internes : définis chaque invariant une fois avec toute la précision nécessaire, puis référence-le dans les tests, validations ou critères d'acceptation plutôt que de le reformuler intégralement.

À précision égale, préfère la formulation la plus compacte. Ne raccourcis jamais au prix d'une perte de sens, de contrainte ou de nuance utile.

Ne cherche jamais à atteindre une longueur ou un pourcentage de réduction prédéfini. Un prompt déjà dense peut rester pratiquement inchangé ; une tranche complexe ou expérimentale peut légitimement nécessiter un prompt long.

Une information n'est supprimable comme redondante que si Codex peut la retrouver directement dans une autorité accessible, applicable à la tâche et suffisamment précise. Ne remplace pas une décision explicite propre à la tranche par une inférence.

Conserve les références explicites aux documents que Codex doit lire lorsqu'elles servent à router efficacement son contexte. Référencer une autorité pertinente n'est pas considéré comme une répétition inutile.

Évite les instructions génériques de persona telles que « act as a senior developer » lorsqu'elles peuvent être remplacées par des comportements observables ou sont déjà couvertes par les règles du dépôt.

N'ajoute pas au prompt les règles générales déjà présentes dans `AGENTS.md` ou une autre autorité globale, sauf si leur rappel est nécessaire pour lever une ambiguïté spécifique à la tranche.

Avant de rendre le prompt, vérifie mentalement :

1. **Authority test** — une règle ou décision est-elle répétée alors qu'elle existe déjà dans une autorité directement accessible ? Si oui, référence l'autorité plutôt que de la recopier.
2. **Inference test** — supprimer cette information obligerait-il Codex à prendre lui-même une décision propre à la tranche ? Si oui, conserve-la.
3. **Precision test** — la formulation raccourcie perd-elle une frontière, une valeur, une nuance, un cas limite ou une condition ? Si oui, conserve la formulation plus précise.
4. **Duplication test** — le même invariant est-il défini plusieurs fois sous des formulations différentes ? Si oui, garde une définition normative unique et référence-la ensuite.
5. **Execution test** — après lecture du prompt et des autorités référencées, Codex peut-il déterminer sans ambiguïté :

   * l'objectif exact de la tranche ;
   * son périmètre et ses exclusions ;
   * les décisions et invariants nouveaux ;
   * les preuves et validations attendues ;
   * les conditions de réussite ou de blocage ?
6. **Stability test** — le prompt a-t-il durci une hypothèse ou une option discutée en obligation, affaibli une décision établie, ou introduit une nouvelle règle générale qui devrait plutôt vivre dans une autorité du projet ? Si oui, corrige cette dérive.
7. **Documentation test** — le prompt demande-t-il une mise à jour documentaire vague ou
   transforme-t-il implicitement un rapport de run en contenu d'autorité ? Si oui, remplace-la
   par un delta documentaire borné ou supprime la mise à jour lorsqu'aucun état autoritatif ne
   change.

La réduction de tokens est un bénéfice secondaire. La priorité reste la fiabilité du contrat donné à Codex.

---

# Modèle de prompt Codex

Le modèle ci-dessous est une **ossature souple**, pas un formulaire à remplir systématiquement.

N'inclus une section que lorsqu'elle transporte une information utile pour la tranche. Une tâche simple doit pouvoir produire un prompt court ; une tranche complexe peut nécessiter davantage de sections et de détails.

```markdown
# <Phase / tranche — titre précis et explicite>

Lis les autorités pertinentes pour cette tranche, notamment :

- `AGENTS.md` applicable(s), lorsqu'il y en a ;
- `<document pertinent>`
- `<ADR / design doc pertinent>`
- `<contrat ou module précédent pertinent>`

Inspecte ensuite l'état réel du dépôt avant toute implémentation.

## Objectif

<Décrire le résultat unique attendu de cette tranche.>

## Périmètre

Cette tranche couvre :

- <élément>
- <élément>

Hors périmètre :

- <élément réellement important à exclure>
- <élément>

## Invariants et décisions

<Inclure uniquement les décisions, contraintes et frontières propres à cette tranche ou insuffisamment définies dans les autorités existantes.>

- <invariant précis>
- <invariant précis>
- <valeur / seuil / identité / ordering semantics si nécessaire>
- <cas limite ou comportement obligatoire>

## Implémentation

<À utiliser seulement si la manière d'implémenter fait elle-même partie du contrat.>

- <contrainte d'intégration>
- <API/frontière existante à réutiliser>
- <dépendance ou comportement imposé/interdit>

Évite de prescrire des détails d'implémentation lorsque plusieurs solutions seraient également conformes au contrat.

## Preuves / expérimentation

<À utiliser pour les tranches de qualification, d'intégration ou de recherche nécessitant des preuves concrètes.>

- <conditions de l'expérience>
- <nombre de runs / processus / observations>
- <seuils ou fenêtres temporelles>
- <artefacts ou mesures attendus>

## Validation

Tester les invariants et comportements définis ci-dessus, notamment :

- <test comportemental spécifique>
- <cas limite spécifique>
- <preuve d'intégrité / déterminisme / isolation>
- <validation propre à la tranche>

Ne répète pas intégralement les invariants déjà définis ; référence-les ici lorsque cela suffit.

## Acceptation

La tranche est acceptée si :

- <condition observable>
- <condition observable>
- <preuve requise>

Termine en `BLOCKED` si :

- <condition réellement bloquante>
- <impossibilité de satisfaire un invariant obligatoire>
- <absence de preuve nécessaire>

## Impact documentaire

<Uniquement si la tranche peut créer ou modifier sémantiquement une autorité structurée. Omettre
cette section lorsqu'aucun delta documentaire n'est attendu.>

Déclare le delta **par autorité**, sans demander une synchronisation générique de toute la
documentation. Exemples de forme :

- `ROADMAP.md` : <statut / gate / prochaine étape réellement affectés, ou `no change expected`>
- `CODEBASE_MAP.md` : <ownership / chemin / dépendance stable réellement affectés, ou `no change expected`>
- `<phase / contract / architecture / qualification>` : <delta précis>

Si `maintain-project-authorities` est installé, l'utiliser pour appliquer ces changements. Le
skill route la politique depuis le corpus projet sous `docs/engineering/`. S'il n'est pas
disponible, lire directement `docs/engineering/DOCUMENTATION_MODEL.md` et le guide du type de
document concerné. Ne pas supposer que les fichiers de prompt/review du dépôt de workflow ont été
copiés dans le projet.

Après le run :

- ne modifier une autorité que si le fait accepté qu'elle possède a réellement changé ;
- remplacer l'état supersédé des autorités vivantes au lieu d'y accumuler la chronologie du run ;
- router la preuve détaillée vers les qualifications et le détail de phase vers le plan de phase ;
- si un impact documentaire imprévu exige une nouvelle décision structurante, ne pas l'inventer
  silencieusement : le rendre explicite et terminer `BLOCKED` lorsque cette décision est
  nécessaire à la conformité de la tranche.

## Compte rendu final

Demande un compte rendu final détaillé, factuel et structuré, servant de
handoff pour une revue indépendante dans ChatGPT.

Le rapport doit permettre de comprendre précisément ce qui a été fait et de
vérifier les affirmations importantes sans devenir une répétition du prompt.

Inclure selon la tranche :

- changements réellement effectués ;
- fichiers et frontières concernés ;
- décisions prises pendant l'implémentation et leur justification ;
- comportement observé et preuves obtenues ;
- commandes de validation exécutées et résultats ;
- résultats des captures, expériences ou mesures lorsque pertinentes ;
- écarts éventuels par rapport au plan initial ;
- limitations, hypothèses et incertitudes restantes ;
- documentation et roadmap mises à jour ;
- état final du dépôt ;
- message de commit recommandé.

Ne masque pas un résultat incomplet derrière un résumé positif.
Distingue clairement ce qui a été démontré, observé, supposé ou laissé pour une
tranche ultérieure.

Termine par `<READY_FOR_REVIEW ou autre statut défini pour la tranche>` si les critères sont satisfaits, sinon par `BLOCKED`.
```

## Principes d'utilisation du modèle

Le prompt final ne doit pas chercher à remplir toutes les sections pour respecter la forme.

Supprime toute section sans contenu substantiel.

Fusionne des sections lorsqu'elles couvrent naturellement le même contrat.

Ne répète pas les règles permanentes du dépôt.

Lorsqu'une section `Impact documentaire` est nécessaire, traite-la comme un contrat de delta :
elle borne **ce qui peut changer**, elle ne demande pas de recopier le rapport final dans les
autorités. Une preuve produite par le run n'implique pas à elle seule une modification de roadmap,
architecture, codebase map ou contrat.

Ne transforme pas une suggestion, une hypothèse ou une possibilité explorée pendant la
discussion en obligation de tranche sans décision explicite. Inversement, ne rends pas
facultative une contrainte qui a été clairement arrêtée.

Ne recopies pas le contenu d'un ADR, d'une architecture ou d'un design doc lorsqu'une référence précise suffit.

En revanche, ne délègue pas à ces documents une décision qui n'y est pas réellement établie.

Pour une tranche complexe, préfère quelques invariants complets et normatifs à de nombreuses reformulations partielles du même invariant.

Les listes de tests doivent démontrer le contrat, pas le redéfinir.

Les conditions `BLOCKED` doivent couvrir les véritables impossibilités ou violations du contrat, pas répéter mécaniquement chaque exigence du prompt.

Le compte rendu final doit demander les éléments nécessaires à la revue de la tranche sans imposer une restitution exhaustive de tout ce que Codex vient de faire.

La longueur finale du prompt doit être déterminée par la quantité réelle d'information nouvelle nécessaire à la tranche, jamais par une cible de tokens.
