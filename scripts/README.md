```markdown
[![CI](https://github.com/mrouanet31/specflow/actions/workflows/ci.yml/badge.svg)](https://github.com/mrouanet31/specflow/actions/workflows/ci.yml)

# GitHub Issue Importer

Petit utilitaire pour importer des issues depuis un CSV vers un dépôt GitHub.

Fichiers

- `github_issue_importer.py` : script principal.
- `*.csv` : fichiers d'entrée (ex : `phase1-backlog-import.csv`).

Prérequis

- Python 3.8+
- pip install requests
- Un token GitHub avec scope `repo` (pour dépôts privés) ou `public_repo` (pour dépôts publics).

Sécurité

- NE COMMITEZ PAS votre token. Exportez-le dans votre shell avant d'exécuter :

```bash
export GITHUB_TOKEN=ghp_xxx
```

Usage

Basic (dry-run) :

```bash
python3 scripts/github_issue_importer.py --dry-run owner/repo path/to/backlog.csv
```

Import réel (skip existing, create missing labels, concurrency 3, save results) :

```bash
export GITHUB_TOKEN=ghp_xxx
python3 scripts/github_issue_importer.py owner/repo path/to/backlog.csv \
  --skip-existing --create-labels --label-estimate --concurrency 3 --output-file results.csv
```

Options clés

- `--dry-run` : n'effectue pas de création, affiche juste ce qui serait fait.
- `--skip-existing` : vérifie si un issue du même titre existe et évite la création.
- `--create-labels` : crée automatiquement des labels manquants.
- `--label-estimate` : ajoute un label `estimate:<value>` si la colonne `estimate` est présente.
- `--milestone "Title"` : assigne ou crée un milestone global pour toutes les issues.
- `--concurrency N` : nombre de travailleurs parallèles (1 par défaut).
- `--output-file` : CSV résultat listant status par ligne (par défaut `import-results.csv`).
- `--verbose` : logs détaillés.

CSV attendu

- Colonnes recommandées (en-têtes) : `title`, `body`, `estimate`, `labels`, `assignee`, `milestone`
- `labels` peut être séparé par `,` ou `;`.
- `assignee` peut contenir plusieurs logins séparés par `,`.
- `milestone` peut être défini par ligne (prioritaire) ou en option globale `--milestone`.

Limitations & conseils

- Rate limits : pour gros imports, utilisez `--concurrency 1` et augmentez `--sleep` pour réduire les risques de throttling.
- Permissions : le token doit pouvoir créer labels/milestones (scope `repo`). Les assignees doivent être membres du dépôt sinon l'assignation échouera.
- skip-existing utilise l'API de recherche GitHub et peut renvoyer faux positifs/limites de rate.
- Pour très gros imports, considérez un script utilisant GraphQL ou découpez votre CSV en lots.

Exemple rapide

```bash
export GITHUB_TOKEN=ghp_xxx
python3 scripts/github_issue_importer.py myorg/specflow phase1-backlog-import.csv --create-labels --label-estimate --skip-existing --concurrency 2
```

Support & améliorations possibles

- Ajouter mapping estimate -> story points (champ spécial) au lieu de label
- Utiliser GraphQL pour performance
- Supporter création de milestones par colonne plus avancée

---

Fichier README pour l'utilitaire d'import d'issues.

```
# GitHub Issue Importer

Petit utilitaire pour importer des issues depuis un CSV vers un dépôt GitHub.

Fichiers

- `github_issue_importer.py` : script principal.
- `*.csv` : fichiers d'entrée (ex : `phase1-backlog-import.csv`).

Prérequis

- Python 3.8+
- pip install requests
- Un token GitHub avec scope `repo` (pour dépôts privés) ou `public_repo` (pour dépôts publics).

Sécurité

- NE COMMITEZ PAS votre token. Exportez-le dans votre shell avant d'exécuter :

```bash
export GITHUB_TOKEN=ghp_xxx
```

Usage

Basic (dry-run) :

```bash
python3 scripts/github_issue_importer.py --dry-run owner/repo path/to/backlog.csv
```

Import réel (skip existing, create missing labels, concurrency 3, save results) :

```bash
export GITHUB_TOKEN=ghp_xxx
python3 scripts/github_issue_importer.py owner/repo path/to/backlog.csv \
  --skip-existing --create-labels --label-estimate --concurrency 3 --output-file results.csv
```

Options clés

- `--dry-run` : n'effectue pas de création, affiche juste ce qui serait fait.
- `--skip-existing` : vérifie si un issue du même titre existe et évite la création.
- `--create-labels` : crée automatiquement des labels manquants.
- `--label-estimate` : ajoute un label `estimate:<value>` si la colonne `estimate` est présente.
- `--milestone "Title"` : assigne ou crée un milestone global pour toutes les issues.
- `--concurrency N` : nombre de travailleurs parallèles (1 par défaut).
- `--output-file` : CSV résultat listant status par ligne (par défaut `import-results.csv`).
- `--verbose` : logs détaillés.

CSV attendu

- Colonnes recommandées (en-têtes) : `title`, `body`, `estimate`, `labels`, `assignee`, `milestone`
- `labels` peut être séparé par `,` ou `;`.
- `assignee` peut contenir plusieurs logins séparés par `,`.
- `milestone` peut être défini par ligne (prioritaire) ou en option globale `--milestone`.

Limitations & conseils

- Rate limits : pour gros imports, utilisez `--concurrency 1` et augmentez `--sleep` pour réduire les risques de throttling.
- Permissions : le token doit pouvoir créer labels/milestones (scope `repo`). Les assignees doivent être membres du dépôt sinon l'assignation échouera.
- skip-existing utilise l'API de recherche GitHub et peut renvoyer faux positifs/limites de rate.
- Pour très gros imports, considérez un script utilisant GraphQL ou découpez votre CSV en lots.

Exemple rapide

```bash
export GITHUB_TOKEN=ghp_xxx
python3 scripts/github_issue_importer.py myorg/specflow phase1-backlog-import.csv --create-labels --label-estimate --skip-existing --concurrency 2
```

Support & améliorations possibles

- Ajouter mapping estimate -> story points (champ spécial) au lieu de label
- Utiliser GraphQL pour performance
- Supporter création de milestones par colonne plus avancée

---

Fichier README pour l'utilitaire d'import d'issues.
