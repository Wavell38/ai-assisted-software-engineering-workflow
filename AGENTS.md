# Maintenance du dépôt de workflow

Ce dépôt distribue des procédures et ressources communes ; il ne contient pas les
autorités des projets consommateurs.

## Responsabilités

- `ENGINEERING_WORKFLOW.md` porte le processus général et `DOCUMENTATION_MODEL.md`
  la répartition des autorités, de l'état courant, des décisions et des preuves.
- Les dossiers documentaires portent les guides et templates de chaque type.
- `review/maintain-project-authorities/SKILL.md` porte la procédure documentaire ;
  `review/review-and-remediate/SKILL.md` porte la gate et ses cinq profils TOML.
- `agents/AGENTS_BASE_TEMPLATE.md` aide à définir les règles propres à un projet.
  Les instructions globales distribuées sont distinctes du présent fichier.
- `scripts/install.py` assemble et installe les ressources ; `tests/` vérifie ce
  contrat dans des répertoires temporaires. `README.md` décrit leur utilisation.
- `VERSION` est l'unique version du corpus, selon la politique du README.

## Discipline de modification

Conserver les emplacements sources sauf nécessité concrète. Modifier la source
responsable d'une règle et corriger ses références affectées sans dupliquer la
procédure. Préserver les rôles, modèles et efforts de raisonnement des reviewers.
Les liens des bundles se résolvent depuis le skill installé ; vérifier aussi leur
routage depuis le dépôt source. Charger seulement les guides utiles à la tâche.

Appliquer la maintenance documentaire aux changements sémantiques et la procédure
de review/remédiation après validation. Les sources du présent dépôt permettent
de travailler sur le workflow même si l'installation globale est plus ancienne.

## Installation et validation

L'installateur utilise Python 3.11+ et uniquement sa bibliothèque standard, sous
Windows et Ubuntu. Il respecte le home utilisateur et `CODEX_HOME`, reste hors
réseau et ne modifie jamais les projets consommateurs. Préserver le contenu
personnel, sauvegarder les reprises sans propriété établie, refuser les conflits
et les chemins liés dangereux, et garder `--check` sans écriture.

Exécuter `python -B -m unittest discover -s tests -v` après modification de
l'installation ou de ses ressources. Vérifier les bundles, TOML, liens, reprises,
échecs et idempotence. Ne jamais tester dans le véritable environnement Codex sans
autorisation explicite. Rapporter la plateforme exécutée et les limites restantes.
Ne pas committer, taguer ou pousser sans demande explicite.
