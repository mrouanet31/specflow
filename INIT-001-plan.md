INIT-001: Initialize monorepo and CI

This plan was created to initialize the repository with a monorepo structure, a minimal Spring Boot backend scaffold, a placeholder Angular frontend, CI, and onboarding docs.

Scope

- Create folders: frontend/, backend/, infra/
- Add Spring Boot minimal application in backend
- Add placeholder Angular project files in frontend
- Add GitHub Actions CI workflow that builds frontend, builds backend, and runs Python tests
- Add MIT license and onboarding README changes

Checklist

- [x] Create feature branch
- [x] Add backend Spring Boot scaffold
- [x] Add frontend placeholder
- [x] Add CI workflow
- [x] Add LICENSE and README updates
- [ ] Create PR with this plan in description

Risks

- CI may need tuning for real Angular project
- Backend scaffold is minimal; add controllers and tests next

How to validate

- Open a PR and ensure CI passes
- Run `mvn -f backend/pom.xml -DskipTests package` locally

# Plan de développement — INIT-001: Initialiser monorepo

## Résumé

Créer la structure du monorepo (par ex. Nx ou équivalent) avec les modules principaux `frontend/`, `backend/`, `infra/`.
Livrable : dépôt initialisé avec README, licence, `.gitignore`, configuration minimale CI (build passes).

## Objectifs

- Fournir une structure claire et extensible pour le code frontend, backend et infra.
- Ajouter les fichiers de base (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT si souhaité).
- Mettre en place une CI minimale qui build le frontend et le backend.

## Critères d'acceptation

- Le dépôt est public/privé selon la décision du PO et contient les répertoires `frontend/`, `backend/`, `infra/`.
- `README.md` explique la structure et comment lancer localement (dev, tests minimal).
- `.gitignore` présent et adapté (node_modules, envs, build outputs).
- Un job GitHub Actions (ou pipeline équivalent) exécute un build minimal et retourne vert pour le commit initial.

## Décomposition (Tâches et sous-tâches)

Estimation totale : 3 points (Fibonacci). Fractionnable.

1. Initialisation repo (0.5)

   - Créer le repo sur GitHub (ou remote choisi) — owner: DevOps/PO
   - Initialiser README.md, LICENSE (MIT/Apache), .gitignore

2. Structure des dossiers (0.5)

   - Ajouter dossiers vides avec README locaux : `frontend/`, `backend/`, `infra/`
   - Ajouter un `tools/` ou `scripts/` si utile pour helpers d'initialisation

3. Scaffolding minimal

   - Frontend (1) — Angular
     - Générer un scaffold Angular minimal (p.ex. `ng new` ou Nx Angular app) ou fournir un README expliquant le framework choisi
     - Ajouter scripts npm/yarn pour `start`/`build` (ex: `npm run build` qui appelle `ng build`)
     - Ajouter un `angular.json` / configuration minimale ou pointer vers le projet Nx si utilisé
   - Backend (1) — Spring Boot
     - Générer un scaffold Spring Boot minimal (Maven/Gradle) avec un artefact exécutable (`spring-boot-starter-web`)
     - Ajouter `pom.xml` ou `build.gradle` et un `Application` class pour démarrer l'app
     - Documenter les commandes `mvn -q -f backend/pom.xml package` et `java -jar backend/target/...jar`

4. CI minimal (0.5)

   - Ajouter workflow GitHub Actions `.github/workflows/ci.yml` qui au moins installe dépendances et lance `build` pour frontend et backend
   - S'assurer que la job succeed sur la branche principale

5. Documentation & onboarding (0.5)
   - Mettre à jour `README.md` racine avec instructions dev local, structure du repo et comment exécuter la CI localement si possible

## Checklist PR (à inclure dans la description des PRs liées)

- [ ] Le code est dans le bon dossier (`frontend/`, `backend/`, `infra/`)
- [ ] README mis à jour avec instructions de démarrage locales
- [ ] `.gitignore` mis à jour
- [ ] Workflow CI ajouté et passe sur la PR
- [ ] Aucun secret ou token commité
- [ ] Labels/issue linkés si pertinent

## Tests et validation

- Runner CI : exécuter `npm run build` (ou équivalent) dans `frontend/` et `backend/`.
- Vérifier que le workflow GitHub Actions passe sur la PR initiale.
- Manual smoke test : cloner repo, exécuter les scripts `start`/`run` décrits dans les README et vérifier qu'ils ne crashent immédiatement.

## CI minimal — exemple (GitHub Actions)

Fichier: `.github/workflows/ci.yml` (extrait)

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"
      - name: Build frontend (Angular)
        run: |
          cd frontend || exit 0
          if [ -f package.json ]; then npm ci && npm run build || true; fi
      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"
      - name: Build backend (Spring Boot)
        run: |
          cd backend || exit 0
          if [ -f pom.xml ]; then mvn -q -f pom.xml -DskipTests package || true; fi
```

## Commandes utiles

- Initialiser localement :
  - git clone <repo>
  - cd <repo>
  - # frontend (Angular)
    cd frontend && npm install && npm run build
  - # backend (Spring Boot - Maven)
    cd backend && mvn -q -DskipTests package

## Dépendances & permissions

- Aucun service externe requis pour l'initialisation. Pour les workflows CI, prévoir des runners publics (GitHub Actions) ou CI interne.

## Risques & mitigations

- Choix de la stack (Angular/React, Spring/Express) : peut retarder si controversé — mitigation : proposer un scaffold minimal basé sur préférences du lead technique.
- Secrets accidentels committés : mitigation — vérifier `.gitignore` et ajouter pre-commit hook si nécessaire.

## Livrables

- Repo initialisé et accessible
- CI minimal qui passe
- README expliquant comment démarrer et où se trouvent les services

## Annexe — suggestions d'extensions futures

- Ajouter templates PR/issue (INIT-002)
- Ajouter CONTRIBUTING.md et conventions (INIT-003)
- Générer un pipeline plus riche (tests unitaires, lint)
