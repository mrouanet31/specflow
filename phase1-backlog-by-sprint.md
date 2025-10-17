# Backlog Phase 1 — Sprint par sprint

Ce document découpe le plan Phase 1 (MVP) en stories prêtes à être importées dans un backlog (GitHub Issues/Jira).

Notation estimations : Fibonacci (1,2,3,5,8,13). Owner recommandé = role type (Backend/Frontend/DevOps/Designer/QA).

---

## Sprint 0 — Préparatoire (1 semaine)

1. INIT-001 — Initialiser monorepo
   - Estim: 3
   - Owner: DevOps, Backend, Frontend
   - Description: Créer la structure Nx (ou monorepo équivalent) avec modules `frontend/`, `backend/`, `infra/`.
   - Acceptance:
    - Status: Done
    - Delivered:
       - Repo scaffold (frontend/, backend/, infra/) added
       - README, LICENSE, .gitignore added
       - CI workflow (build frontend, backend, python tests) added and adjusted to use Gradle for backend
       - Frontend scaffold: Angular 20 app added (buildable)
       - Backend scaffold: Spring Boot (Gradle) app added with /health endpoint and tests
       - Feature branch `feature/INIT-001-initialize-monorepo` created and PR merged into `main` (see recent commits)
    - Acceptance:
       - Repo scaffold present and CI builds (see commit history)
   - Dépendances: aucune

2. INIT-002 — Templates PR & Issue
   - Estim: 1
   - Owner: PO
   - Description: Ajouter PR template et issue template (bug/feature) au repo.
   - Acceptance: templates présents et utilisés sur une PR test

3. INIT-003 — Conventions & Coding standards
   - Estim: 2
   - Owner: Tech Lead
   - Description: Documenter conventions (formatting, lint rules, commit messages, branch strategy).
   - Acceptance: document `CONTRIBUTING.md` ajouté

4. INIT-004 — Provisionnement env dev/staging
   - Estim: 5
   - Owner: DevOps
   - Description: Provisionner namespace K8s pour dev/staging (ou Docker Compose pour MVP léger), secrets skeleton
   - Acceptance: staging accessible, secrets manager connecté

5. INIT-005 — Esquisser schéma DB initial
   - Estim: 2
   - Owner: Backend
   - Description: Créer diagramme entité (User, Project, Spec, Task, Constitution) et scripts Flyway baseline
   - Acceptance: migration baseline s'exécute localement

---

## Sprint 1 — Infra & Auth (2 semaines)

1. INFRA-101 — CI pipeline PR checks
   - Estim: 5
   - Owner: DevOps
   - Description: GitHub Actions PR pipeline: build backend, build frontend, unit tests, lint
   - Acceptance: PR pipeline vert sur commit de test

2. INFRA-102 — Docker images & publish
   - Estim: 3
   - Owner: DevOps
   - Description: Dockerfile pour backend et frontend, publish to GH Packages or registry
   - Acceptance: images publiées avec tag

3. AUTH-111 — Implémenter endpoint /api/auth/login
   - Estim: 5
   - Owner: Backend
   - Description: Login avec email/password, password hashing (bcrypt/argon2), return access + refresh tokens
   - Acceptance: tests unitaires et integration valident flow
   - Dépendances: DB baseline

4. AUTH-112 — Implémenter refresh token flow
   - Estim: 3
   - Owner: Backend
   - Description: Endpoint /api/auth/refresh pour renouveler access token
   - Acceptance: flow refresh testé

5. AUTH-113 — RBAC & role model
   - Estim: 3
   - Owner: Backend
   - Description: Add roles (ADMIN, USER, VIEWER) and middleware annotations
   - Acceptance: endpoints sécurisés par rôle

6. INFRA-103 — Provisionnement Postgres staging
   - Estim: 2
   - Owner: DevOps
   - Description: Provision Postgres instance for staging, apply Flyway baseline
   - Acceptance: DB accessible and migrations applied

7. SEC-120 — Secrets integration
   - Estim: 2
   - Owner: DevOps
   - Description: Integrate GitHub Actions secrets with Vault/managed secrets
   - Acceptance: CI can pull secrets to run integration tests

---

## Sprint 2 — Infra Stabilisation & WebSocket (2 semaines)

1. INFRA-201 — Monitoring basic (Prometheus)
   - Estim: 3
   - Owner: DevOps
   - Description: Expose /actuator/prometheus metrics, configure Prometheus scraping
   - Acceptance: metrics visible in Prometheus

2. INFRA-202 — Central logging skeleton
   - Estim: 3
   - Owner: DevOps
   - Description: Configure structured logging (JSON) and central collection (Loki/ELK outline)
   - Acceptance: sample logs visible in central system

3. WS-210 — WebSocket skeleton (Spring WebSocket)
   - Estim: 5
   - Owner: Backend
   - Description: Implement WS endpoint with ping/pong and a simple pub/sub channel for notifications
   - Acceptance: frontend can connect and receive ping

4. INFRA-203 — Helm chart minimal / k8s manifests
   - Estim: 5
   - Owner: DevOps
   - Description: Create Helm chart with deployment/service/ingress minimal
   - Acceptance: app deployable via helm to staging

5. OPS-205 — Backup plan DB for staging
   - Estim: 1
   - Owner: DevOps
   - Description: Schedule backup snapshot for staging DB
   - Acceptance: backup exists and restore tested

---

## Sprint 3 — Constitution Manager (2 semaines)

1. CONST-301 — API CRUD /api/constitutions
   - Estim: 8
   - Owner: Backend
   - Description: Endpoints create, read, update, delete, list; versioning table ConstitutionVersion
   - Acceptance: integration tests cover CRUD + version creation
   - Dépendances: DB migrations

2. CONST-302 — Markdown editor integration (frontend)
   - Estim: 8
   - Owner: Frontend
   - Description: Integrate Monaco or ngx-markdown editor with preview and autosave draft
   - Acceptance: editor displays, preview updates, save persists via API

3. STORAGE-310 — Attachments storage (S3-compatible)
   - Estim: 3
   - Owner: DevOps, Backend
   - Description: Implement attachments upload endpoint and storage backed by S3 or PVC
   - Acceptance: upload/download works in staging

4. EXPORT-320 — Export MD/PDF
   - Estim: 3
   - Owner: Backend
   - Description: Implement export to MD and simple PDF generation (wkhtmltopdf or similar)
   - Acceptance: exported files downloadable

5. TEST-330 — Tests integration API Constitutions
   - Estim: 3
   - Owner: QA, Backend
   - Description: Add integration tests for endpoints
   - Acceptance: CI runs integration tests green

---

## Sprint 4 — Workshop basique & Kanban (2 semaines)

1. WS-401 — Collaborative editing (optimistic updates)
   - Estim: 8
   - Owner: Frontend, Backend
   - Description: Implement optimistic edit flow via WebSocket, simple locking fallback
   - Acceptance: two clients editing see near-real-time updates and conflict handled

2. IA-410 — Assistant stub endpoint
   - Estim: 2
   - Owner: Backend
   - Description: Provide a stub endpoint to return suggestion templates for spec sections
   - Acceptance: frontend can call and display suggestions

3. KANBAN-420 — Tasks CRUD & Kanban UI
   - Estim: 8
   - Owner: Frontend, Backend
   - Description: Task model, endpoints, Kanban board with drag & drop (ToDo/InProgress/Done)
   - Acceptance: create/move tasks persist and reflect across users

4. NOTIF-430 — Notification events via WS
   - Estim: 3
   - Owner: Backend
   - Description: Emit events for mentions, comments, task status changes; deliver via WS
   - Acceptance: receiving clients see notifications in real time

---

## Sprint 5 — Design system & QA (2 semaines)

1. UI-501 — Design system tokens & Storybook
   - Estim: 5
   - Owner: Designer, Frontend
   - Description: Define color tokens, typography, spacing; publish basic components in Storybook
   - Acceptance: storybook with core components accessible

2. UI-502 — Integrate Angular Material + Tailwind tokens
   - Estim: 3
   - Owner: Frontend
   - Description: Configure Tailwind + Angular Material theme with tokens
   - Acceptance: theme applied site-wide

3. QA-510 — E2E scenarios (Cypress)
   - Estim: 5
   - Owner: QA, Frontend
   - Description: Implement E2E smoke tests: login, create constitution, create task, live update
   - Acceptance: tests green in CI

4. ACCESS-520 — Accessibility checks
   - Estim: 2
   - Owner: Designer, Frontend
   - Description: Run basic a11y checks (contrast, keyboard nav) and fix critical issues
   - Acceptance: major a11y issues resolved

---

## Sprint 6 — Launch & docs (2 semaines)

1. DOCS-601 — Developer README + API OpenAPI
   - Estim: 3
   - Owner: Backend, Frontend
   - Description: Write developer README, generate OpenAPI spec for APIs
   - Acceptance: README clear, OpenAPI accessible via /api/docs

2. RUNBOOK-610 — Playbook deploy & rollback
   - Estim: 3
   - Owner: DevOps
   - Description: Create deployment checklist, rollback steps, and runbook for incidents
   - Acceptance: runbook reviewed and stored

3. PERF-620 — Smoke load testing
   - Estim: 3
   - Owner: DevOps, QA
   - Description: Run basic load tests (smoke) on staging (auth + read paths)
   - Acceptance: p95 latency within target or documented issues

4. RELEASE-630 — Release candidate & checklist
   - Estim: 2
   - Owner: PO
   - Description: Prepare release notes, checklist, and validation sign-off
   - Acceptance: PO sign-off for release candidate

---

## Notes & priorités

- Prioriser infra/auth et DB dès Sprint 0–1 pour débloquer développement parallèle frontend.
- Mettre en place feature flags pour IA et WebSocket si besoin.
- Lister tasks cross-sprints (security audit, code quality) comme backlog technique prioritaire.

---

Fichier créé pour être importé en backlog (GitHub/Jira). Peux-l'on maintenant :

- générer les issues GitHub automatiquement (CSV/JSON) ?
- découper davantage certaines stories en sous-tâches ?
