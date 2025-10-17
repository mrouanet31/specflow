## Phase 1 — MVP (3 mois) : Plan d'implémentation

## Objectif

Livrer un MVP opérationnel en 3 mois (6 sprints de 2 semaines) couvrant :

- Infrastructure & CI/CD
- Authentification JWT et RBAC de base
- Base de données & migrations
- Constitution Manager (éditeur Markdown + versioning)
- Specification Workshop (éditeur collaboratif basique)
- Task Kanban
- Notifications temps réel
- Design system minimal et tests E2E

## Hypothèses

- Équipe disponible : 2 backend, 2 frontend, 1 designer, 0.5 DevOps (peut être partagé)
- Sprints de 2 semaines, définition "done" commune
- Tech stack : Angular (frontend), Spring Boot (backend), PostgreSQL, Redis, RabbitMQ
- CI/CD : GitHub Actions, déploiement en staging sur Kubernetes

## Calendrier global

- Semaine 0 (Sprint 0, 1 semaine) : Architecture détaillée, setup monorepo, conventions, backlog initial
- Sprints 1–2 (Semaines 1–4) : Infrastructure & Auth (core infra, CI/CD, DB, JWT)
- Sprints 3–4 (Semaines 5–8) : Core features (Constitution Manager, Workshop basique, Kanban)
- Sprints 5–6 (Semaines 9–12) : Polish & Launch (Design system, E2E, documentation, déploiement)

## Organisation des rôles (rôles, pas noms)

- Product Owner (PO) : priorisation backlog, critères d'acceptation
- Tech Lead Backend : API design, DB, sécurité
- Tech Lead Frontend : UI/UX, composants, intégration
- DevOps / SRE : infra, CI/CD, monitoring
- Designer : design system, composants, accessibility
- QA : tests E2E, définition des scénarios

## Définition de Done (générale)

Une story est « done » quand :

- Code review passée et mergée
- Tests unitaires couvrant les cas critiques existent
- Scénario E2E principal verte en CI pour la fonctionnalité
- Documentation minimale (README + API) mise à jour
- Déployée en staging et validée manuellement par PO

## Sprint-by-sprint (détails)

Sprint 0 (préparatoire - 1 semaine)

- Objectifs : Setup monorepo, conventions, pipeline minimal, backlog affinage
- Tâches :
  - Initialiser monorepo (Nx ou alternative), structure frontend/backend
  - Choisir outils de CI/CD, secrets management (GitHub Actions + Vault)
  - Esquisser schéma DB initial et entités clés (User, Project, Spec, Task, Constitution)
  - Règles de codage, PR template, issue template
  - Provisionnement cluster dev/staging (K8s namespaces)
- Critères d'acceptation : monorepo créé, pipeline CI minimal passe (build), README dev prêt

Sprint 1 (Infra & Auth — 2 semaines)

- Objectifs : CI/CD complet pour build/test, API Auth JWT, DB initiale
- Tâches :
  - CI : build backend (maven/gradle), build frontend (ng), tests unitaires basiques
  - Auth : endpoints /api/auth/login, /api/auth/refresh, JWT setup (refresh token), password hashing
  - RBAC minimal : roles (ADMIN, USER, VIEWER), annotation Spring Security
  - DB : scripts de migration Flyway (baseline), provisionnement Postgres en staging
  - Secrets : intégration secrets GitHub Actions -> Vault/Secrets
- Estimations (grosso modo) : 12–16 points backend, 4 points infra
- Critères d'acceptation : login->JWT flow testé (unit+integration), CI green, DB migrée

Sprint 2 (Infra & Stabilisation — 2 semaines)

- Objectifs : Observabilité, logging, base infra, WebSocket minimal
- Tâches :
  - Monitoring basique (Prometheus metrics exposées, alerting rule simple)
  - Central logging (ELK/Fluentd path outline)
  - WebSocket endpoint skeleton (Spring WebSocket) et ping/pong
  - Docker images versionnées, k8s manifests Helm chart minimal
  - Backup plan DB pour staging
- Critères d'acceptation : endpoints supervisés, Docker images déployées en staging, WS fonctionnel

Sprint 3 (Core Features — 2 semaines)

- Objectifs : Constitution Manager (MVP) + APIs CRUD
- Tâches :
  - Backend : API CRUD /api/constitutions, versioning (ConstitutionVersion), validations
  - Frontend : éditeur markdown (Monaco ou ngx-markdown), preview, sauvegarde draft
  - Storage : attachments minimal (S3-compatible ou PVC), export MD/PDF
  - Tests unitaires et intégration API
- Estimation : backend 10 pts, frontend 10 pts
- Critères d'acceptation : créer/éditer/versionner constitution depuis UI + API OK, export MD

Sprint 4 (Core Features — 2 semaines)

- Objectifs : Specification Workshop basique + Task Kanban
- Tâches :
  - Workshop : éditeur collaboratif basique (lock / optimistic updates) via WebSocket
  - Assistant IA (dégradé) : endpoint stub pour suggestions (intégration ultérieure GPT/Claude)
  - Kanban : CRUD tâches, colonnes (ToDo, InProgress, Done), liaison spec->task
  - UI : composants Kanban, drag & drop
  - Notifications : événements basiques pour changement statut
- Critères d'acceptation : utilisateurs peuvent collaborer en temps réel sur un doc, créer tâches depuis spec, kanban fonctionnement

Sprint 5 (Polish — 2 semaines)

- Objectifs : Design system, accessibilité, tests E2E initiaux
- Tâches :
  - Design system minimal (tokens couleur, spacing, typographie) + Storybook
  - Intégrer Angular Material + Tailwind tokens
  - Scénarios E2E Cypress : login, create constitution, create task, live update
  - QA pass sur staging
- Critères d'acceptation : composants réutilisables publiés, E2E green en CI

Sprint 6 (Launch — 2 semaines)

- Objectifs : Documentation, runbooks, préparation release, corrections critiques
- Tâches :
  - Docs dev + README + API OpenAPI spec
  - Playbook déploiement + rollback
  - Tests de charge basique (smoke load), tuning connexions DB
  - Préparer release notes et checklist
- Critères d'acceptation : release candidate déployée en staging, checklist validée par PO

## Backlog technique (epics & stories prioritaires)

- EPIC: Infrastructure & CI

  - Story: CI pipeline build/test/deploy
  - Story: Docker + K8s manifests
  - Story: Monitoring + Alerting

- EPIC: Auth & Security

  - Story: JWT auth + refresh
  - Story: RBAC middleware
  - Story: Security tests (OWASP basics)

- EPIC: Constitution Manager

  - Story: Markdown editor + preview
  - Story: Versions & diff
  - Story: Export MD/PDF

- EPIC: Workshop & Collaboration

  - Story: WebSocket collaboration core
  - Story: Commenting & inline notes

- EPIC: Kanban & Tasks

  - Story: CRUD + drag & drop
  - Story: Auto-generation tasks from spec (MVP: template-based)

- EPIC: Notifications
  - Story: Real-time events
  - Story: Notification center (UI)

## Non-functional requirements

- Performance : p95 API < 200ms pour endpoints simples
- Scalabilité : architecture stateless pour services, Redis pour sessions si besoin
- Sécurité : OWASP Top10 mitigations, JWT best practices (short lived access tokens)
- Backup/RPO : sauvegarde quotidienne, RTO cible 2h pour staging

## CI/CD & Déploiement

- Branching : trunk-based (main + short-lived feature branches)
- Pipelines :
  - PR: build + unit tests + lint
  - Merge: build + integration tests + image publish
  - Release: deploy to staging + E2E tests
- Rollback : images taggés semver, helm rollback supporté

## Base de données & Migrations

- Tooling : Flyway ou Liquibase (préférer Flyway pour simplicité)
- Process : migrations versionnées dans repo backend, appliquées automatiquement en CI/CD
- Seeds : jeux de données pour dev et staging

## Sécurité & Auth (détails)

- Flow JWT : /login -> access token (15min) + refresh token (7d) stocké côté serveur ou HttpOnly cookie
- Protections : rate limiting, password hashing (bcrypt/argon2), account lockout
- RBAC : annotations sur endpoints, vérification côté backend

## Tests & QA

- Tests unitaires : coverage minimale 60% pour backend critique
- Tests d'intégration : endpoints Auth, Constitutions, Tasks
- E2E : Cypress scenarios smoke pour chaque release
- QA : checklist manuelle avant release + bug triage process

## Monitoring, Logging & Alerting

- Exposer metrics /actuator/prometheus
- Logs structurés JSON -> ELK / Loki
- Alerts : error rate surge, high latency, DB connection errors

## Risques majeurs & mitigations

- Risque : sous-estimation effort IA/Assistant
  - Mitigation : livrer assistant en mode dégradé (stubs) et roadmap d'intégration IA
- Risque : infra K8s trop lourde pour MVP
  - Mitigation : commencer en simple Docker Compose / managed DB, puis migrer
- Risque : intégration WebSocket complexe côté frontend
  - Mitigation : commencer par optimistic updates et polling court terme
- Risque : manque de disponibilité des développeurs clés
  - Mitigation : documentation, pair-programming, backlog remplaçable

## Critères de succès du MVP

- Fonctionnels : un utilisateur peut créer une constitution, collaborer sur une spec, créer une tâche et recevoir une notification en temps réel
- Opérationnels : pipeline CI vert, déploiement en staging automatisé
- Qualité : scénarios E2E critiques verts, review sécurité basique effectuée

## Livrables fin de Phase 1

- Repo monorepo initial avec modules frontend/backend
- Pipelines GitHub Actions configurés
- API Auth + DB + migrations
- Constitution Manager (CRUD + versioning)
- Specification Workshop (collaboration basique)
- Kanban tasks + real-time notifications
- Design system de base + Storybook
- Docs dev + playbook release

## Suivi & reporting

- Daily standup 15m, 2x semaine grooming, review & retro par sprint
- Burndown sprint, velocity tracking (story points)
- Check-ins hebdo PO + Tech Lead

## Prochaines étapes immédiates

1. Valider la composition de l'équipe et engager Sprint 0 (1 semaine)
2. Initialiser monorepo et pipeline CI minimal
3. Finaliser schéma DB et migrations de base

## Annexe : templates rapides

- PR template : summary / changes / how to test / checklist
- Issue template : description / steps to reproduce / acceptance criteria / estimate

---

Fichier créé pour servir de base actionable au démarrage du développement Phase 1 — MVP.
