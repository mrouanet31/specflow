# Backlog Phase 2 — Sprint par sprint

Ce document découpe le plan Phase 2 (Growth) en stories prêtes à être importées dans un backlog (GitHub Issues/Jira).

Notation estimations : Fibonacci (1,2,3,5,8,13). Owner recommandé = role type (Backend/Frontend/DevOps/ML/Designer/QA).

---

## Sprint 1 — Foundations & Discovery (2 semaines)

1. P2-101 — Audit d'intégration MVP
   - Estim: 2
   - Owner: Tech Lead Backend
   - Description: Lister points d'extension dans le MVP (webhooks, API, events, auth) et définir contracts.
   - Acceptance: rapport d'audit avec endpoints cibles et diagramme d'intégration

2. P2-102 — Provisionner vector DB / Elasticsearch
   - Estim: 5
   - Owner: DevOps
   - Description: Déployer instance vector DB (Pinecone/Milvus/OpenSearch) et configurer accès staging
   - Acceptance: index opérationnel et accessible depuis staging

3. P2-103 — Schema d'indexation specs
   - Estim: 3
   - Owner: Backend
   - Description: Définir mapping/metadata (id, version, project, sections, tags, embeddings)
   - Acceptance: mapping documenté et validé par backend

4. P2-104 — PoC ingestion -> embeddings -> retrieval
   - Estim: 8
   - Owner: ML/IA Engineer, Backend
   - Description: Pipeline prototype qui ingère specs, calcule embeddings, stocke et récupère par similarité
   - Acceptance: requête de similarité retourne résultats pertinents pour 5 samples

5. P2-105 — Design marketplace model initial
   - Estim: 3
   - Owner: Designer, PO
   - Description: Définir catalogue, champs metadata, pricing tiers et flow contribution
   - Acceptance: maquette des écrans clefs et modèle de données

---

## Sprint 2 — Technical Plan Builder (MVP) (2 semaines)

1. P2-201 — Endpoint /api/plan-builder
   - Estim: 5
   - Owner: Backend
   - Description: Endpoint qui accepte une spec et renvoie un PlanDraft (JSON schema)
   - Acceptance: endpoint retourne PlanDraft valide pour 3 sample specs

2. P2-202 — Template engine (rule-based)
   - Estim: 8
   - Owner: Backend
   - Description: Implémenter génération de sections à partir de templates (mustache/liquid)
   - Acceptance: 3 templates fonctionnels (microservice, monolith, serverless)

3. P2-203 — Frontend wizard UI
   - Estim: 8
   - Owner: Frontend, Designer
   - Description: Wizard pour saisir paramètres (stack, constraints) et prévisualiser PlanDraft
   - Acceptance: utilisateur peut générer et visualiser PlanDraft depuis UI

4. P2-204 — Export JSON/MD
   - Estim: 3
   - Owner: Backend
   - Description: Exporter PlanDraft en JSON et MD
   - Acceptance: téléchargement export OK

5. P2-205 — Tests & validation
   - Estim: 3
   - Owner: QA, Backend
   - Description: Tests unitaires et integration pour plan-builder
   - Acceptance: tests passent en CI

---

## Sprint 3 — Quality Assurance Dashboard (2 semaines)

1. P2-301 — Data model mapping spec->implementation
   - Estim: 5
   - Owner: Backend
   - Description: Concevoir tables/indices reliant specs, plans, tests, coverage
   - Acceptance: data model documenté et migrations prêtes

2. P2-302 — Endpoint metrics & rules engine
   - Estim: 5
   - Owner: Backend
   - Description: Endpoints pour Spec Completion Score, Risk Heat Map calculs basiques
   - Acceptance: endpoints retournent metrics sample

3. P2-303 — Frontend dashboard widgets
   - Estim: 8
   - Owner: Frontend, Designer
   - Description: Widgets pour coverage, open issues, acceptance checklist
   - Acceptance: dashboard rendu avec données mocks et connecté aux endpoints

4. P2-304 — CI integration for test results ingestion
   - Estim: 5
   - Owner: DevOps, Backend
   - Description: Ingest test results from CI pipelines into dashboard data model
   - Acceptance: sample test results appear in dashboard

---

## Sprint 4 — Git Integration Hub (2 semaines)

1. P2-401 — OAuth connectors (GitHub basic)
   - Estim: 8
   - Owner: Backend, DevOps
   - Description: Implement OAuth flow for GitHub; store tokens securely
   - Acceptance: user can link GitHub account and grant minimal scopes

2. P2-402 — Repo onboarding UI
   - Estim: 5
   - Owner: Frontend
   - Description: UI to select repo, branches and configure sync settings
   - Acceptance: onboarding flow completes and stores config

3. P2-403 — PR creation engine
   - Estim: 8
   - Owner: Backend
   - Description: Given a task/plan, create branch, commit changes and open PR with template
   - Acceptance: PR created in test repo with expected contents

4. P2-404 — Webhooks listener
   - Estim: 5
   - Owner: Backend
   - Description: Listen to repo events (PR merged, CI status) and update spec/task status
   - Acceptance: merging PR updates task status in app

---

## Sprint 5 — SpecGPT alpha & Integrations (2 semaines)

1. P2-501 — IA provider integration & rate limiter
   - Estim: 5
   - Owner: Backend, ML
   - Description: Hook to model provider (OpenAI/Anthropic) with retry and rate limiting
   - Acceptance: provider calls succeed within quotas, errors handled

2. P2-502 — Context builder (RAG) pipeline
   - Estim: 8
   - Owner: ML, Backend
   - Description: Implement RAG: retrieve relevant docs, build prompt, call model
   - Acceptance: suggestions generated for sample specs with context

3. P2-503 — Assistant UI (inline suggestions)
   - Estim: 5
   - Owner: Frontend
   - Description: Inline assistant panel showing suggestions and allowing accept/reject
   - Acceptance: suggestions visible and user can accept to insert into doc

4. P2-504 — Logging & feedback loop
   - Estim: 3
   - Owner: Backend, ML
   - Description: Log model inputs/outputs and user feedback for future training
   - Acceptance: logs stored and accessible for inspection

---

## Sprint 6 — Marketplace structure & Polish (2 semaines)

1. P2-601 — Catalog model & listing API
   - Estim: 5
   - Owner: Backend
   - Description: Implement catalog DB model and listing endpoints with filters/tags
   - Acceptance: listings returned with metadata

2. P2-602 — Marketplace UI (browse & upload)
   - Estim: 8
   - Owner: Frontend, Designer
   - Description: Browse templates, upload new template flow, fork/clone UI
   - Acceptance: upload and fork flows functional in staging

3. P2-603 — Basic moderation tooling
   - Estim: 3
   - Owner: Backend, PO
   - Description: Admin interface to review submissions and accept/reject
   - Acceptance: admin can moderate submissions

4. P2-604 — Legal & TOS skeleton
   - Estim: 1
   - Owner: PO/Legal
   - Description: Add TOS + content policy skeleton
   - Acceptance: TOS page published and linked in UI

5. P2-605 — Polish: docs & demos
   - Estim: 3
   - Owner: PO, Designer
   - Description: Create how-to docs, demo flows and finalize small UX fixes
   - Acceptance: docs published and demo flows available

---

## Cross-sprint & Technical debt tasks

- P2-TD-01 — Security review (OWASP) — Estim 5 — Owner: Backend/DevOps
- P2-TD-02 — Add feature flags system — Estim 3 — Owner: DevOps
- P2-TD-03 — Observability for IA calls (cost & latency) — Estim 3 — Owner: DevOps

---

Fichier créé pour être importé en backlog (GitHub/Jira). Veux-tu que je :

- génère un CSV/JSON prêt pour import GitHub Issues ?
- découpe automatiquement certaines stories en sous-tâches ?
