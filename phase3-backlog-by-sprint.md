# Backlog Phase 3 — Sprint par sprint

Ce document découpe le plan Phase 3 (Scale) en stories prêtes à être importées dans un backlog (GitHub Issues/Jira).

Notation estimations : Fibonacci (1,2,3,5,8,13). Owner recommandé = role type (Backend/Frontend/ML/Mobile/DevOps/Designer/QA).

---

## Trimestre A — Sprints 1–4 (Foundations & MVPs)

### Sprint 1 (2 semaines) — Parallel Explorer: design engine & generator

1. P3-101 — Définir paramètres de génération de variantes
   - Estim: 3
   - Owner: Tech Lead Backend, Product
   - Description: Documenter critères (architecture patterns, DB choices, scaling assumptions, tradeoffs)
   - Acceptance: spec technique pour generator validée

2. P3-102 — Implémenter pipeline generator (spec -> variant artifacts)
   - Estim: 8
   - Owner: Backend
   - Description: Service qui transforme spec en N variantes (squelettes JSON/MD)
   - Acceptance: N=3 variants générés pour 5 sample specs

3. P3-103 — Benchmark harness initial (local)
   - Estim: 5
   - Owner: DevOps, Backend
   - Description: Framework pour exécuter micro-bench sur variantes (latence, mem, simple throughput)
   - Acceptance: harness exécute benchmarks sur generated variants

4. P3-104 — UI comparaison (prototype)
   - Estim: 5
   - Owner: Frontend, Designer
   - Description: Simple table comparant metrics & tradeoffs entre variants
   - Acceptance: UI montre N variants et leurs scores

---

### Sprint 2 (2 semaines) — Data infra & Canvas MVP

1. P3-201 — Data lake & event ingestion (PoC)
   - Estim: 8
   - Owner: DevOps, Backend
   - Description: Setup S3 bucket, Kafka topic (or Kinesis), ETL skeleton (ingest specs, events, test results)
   - Acceptance: events ingested and queryable

2. P3-202 — Implement initial ML tasks (clustering, similarity)
   - Estim: 8
   - Owner: ML Engineer
   - Description: Train small models for spec clustering & similarity search using sample data
   - Acceptance: clustering and similarity APIs return expected results on test set

3. P3-203 — Collaborative Canvas MVP
   - Estim: 5
   - Owner: Frontend, Designer
   - Description: Implement infinite canvas, basic post-its, export to spec
   - Acceptance: export produces a spec draft from canvas content

---

### Sprint 3 (2 semaines) — Parallel Explorer: cost & CI harness

1. P3-301 — Cost & complexity estimator (heuristics)
   - Estim: 5
   - Owner: Backend, ML
   - Description: Implement heuristics to estimate cost/complexity per variant (compute units, infra cost)
   - Acceptance: estimator outputs values for variants and used in UI

2. P3-302 — CI integration for benchmark harness
   - Estim: 5
   - Owner: DevOps
   - Description: Run benchmark harness in ephemeral k8s namespaces via CI for reproducible runs
   - Acceptance: CI job runs harness and stores results

3. P3-303 — Mobile skeleton: auth & view spec
   - Estim: 5
   - Owner: Mobile
   - Description: React Native app skeleton with login and spec viewing
   - Acceptance: mobile app lists specs and opens detail view

---

### Sprint 4 (2 semaines) — Analytics infra & Canvas improvements

1. P3-401 — Feature store & ETL pipelines
   - Estim: 8
   - Owner: ML, DevOps
   - Description: Persist features for model training (spec metrics, acceptance signals)
   - Acceptance: features available for training jobs

2. P3-402 — Canvas: templates & session persistence
   - Estim: 5
   - Owner: Frontend
   - Description: Save canvas sessions, provide template gallery
   - Acceptance: templates usable and sessions reloadable

3. P3-403 — Privacy & PII redaction pipeline for ingestion
   - Estim: 5
   - Owner: Backend, ML
   - Description: Detect and redact PII in specs before storage/embedding
   - Acceptance: redaction applied on ingestion tests

---

## Trimestre B — Sprints 5–8 (Harden & Scale)

### Sprint 5 (2 semaines) — Parallel Explorer v1 & Mobile features

1. P3-501 — Explorer: run automated benchmarks & produce ranking
   - Estim: 8
   - Owner: Backend, DevOps
   - Description: Execute benchmarks, compute combined score and rank variants
   - Acceptance: ranking produced and visible in UI

2. P3-502 — Mobile: comments & offline read
   - Estim: 8
   - Owner: Mobile, Frontend
   - Description: Add ability to comment on specs and cache for offline read
   - Acceptance: comments sync and offline view works

3. P3-503 — Sandbox infra for variant execution (ephemeral)
   - Estim: 8
   - Owner: DevOps
   - Description: K8s namespace provisioning + IaC for ephemeral sandboxes
   - Acceptance: harness can launch sandbox, run variant, teardown

---

### Sprint 6 (2 semaines) — Spec Analytics v1

1. P3-601 — Train time-to-implement model (MVP)
   - Estim: 8
   - Owner: ML Engineer
   - Description: Train model using historical specs and project durations (or synthetic dataset)
   - Acceptance: model predicts relative time-to-implement with baseline accuracy

2. P3-602 — Risk heatmap generation endpoint
   - Estim: 5
   - Owner: Backend, ML
   - Description: Provide endpoint that returns risk scores per spec section
   - Acceptance: endpoint returns heatmap data for sample specs

3. P3-603 — Dashboard integration for analytics
   - Estim: 5
   - Owner: Frontend
   - Description: Surface model outputs in dashboards and spec views
   - Acceptance: analytics visible and explainable to users

---

### Sprint 7 (2 semaines) — Marketplace beta & Canvas features

1. P3-701 — Marketplace: public listing & search (beta)
   - Estim: 8
   - Owner: Backend, Frontend
   - Description: Support public listings, tag-based search and basic ranking
   - Acceptance: users can browse and search templates

2. P3-702 — Marketplace moderation workflow
   - Estim: 5
   - Owner: Backend, PO
   - Description: Admin UI for review queue, accept/reject templates
   - Acceptance: moderation flow functional

3. P3-703 — Canvas: recording & replay (MVP)
   - Estim: 5
   - Owner: Frontend
   - Description: Record canvas sessions with timestamped actions and replay capability
   - Acceptance: recorded session replay works

---

### Sprint 8 (2 semaines) — Marketplace payments & author tools

1. P3-801 — Stripe integration (payments flow, sandbox)
   - Estim: 8
   - Owner: Backend
   - Description: Implement payment flow for paid templates (sandbox mode)
   - Acceptance: test transactions succeed in sandbox

2. P3-802 — Author dashboard (sales metrics MVP)
   - Estim: 5
   - Owner: Frontend, Backend
   - Description: Show basic sales/usage metrics to template authors
   - Acceptance: authors can view metrics for their templates

3. P3-803 — Marketplace discoverability improvements
   - Estim: 5
   - Owner: Frontend, ML
   - Description: Add recommended templates widget based on similarity and popularity
   - Acceptance: recommendations populate for users

---

## Trimestre C — Sprints 9–12 (Public Launch & Optimization)

### Sprint 9 (2 semaines) — Canvas v1 & Marketplace polish

1. P3-901 — Canvas templates marketplace integration
   - Estim: 5
   - Owner: Frontend, Backend
   - Description: Allow saving canvas templates to marketplace and licensing metadata
   - Acceptance: canvas templates can be published to marketplace

2. P3-902 — Marketplace legal & TOS finalization
   - Estim: 3
   - Owner: PO/Legal
   - Description: Finalize TOS, IP policy, revenue share model
   - Acceptance: legal artifacts approved

3. P3-903 — Performance tuning for marketplace (search & CDN)
   - Estim: 5
   - Owner: DevOps
   - Description: Improve search latency and asset delivery via CDN
   - Acceptance: p95 search latency below target

---

### Sprint 10 (2 semaines) — Launch readiness

1. P3-1001 — Scalability runbook & chaos test
   - Estim: 5
   - Owner: DevOps, SRE
   - Description: Run chaos tests for critical workflows and document runbook
   - Acceptance: runbook updated and major failures addressed

2. P3-1002 — Mobile: GA polish & app store prep
   - Estim: 5
   - Owner: Mobile
   - Description: Finalize mobile UX, permissions, build pipelines for app stores
   - Acceptance: app builds ready for submission

3. P3-1003 — Security audit & remediation
   - Estim: 8
   - Owner: Backend, DevOps, QA
   - Description: Perform security audit (internal or 3rd party) and fix critical issues
   - Acceptance: audit report and critical issues fixed

---

### Sprint 11 (2 semaines) — GA launch tasks

1. P3-1101 — Marketing launch checklist execution
   - Estim: 3
   - Owner: PO, Marketing
   - Description: Execute launch tasks (press release, beta invites, demo events)
   - Acceptance: launch assets published

2. P3-1102 — Operational monitoring & SLOs
   - Estim: 3
   - Owner: DevOps
   - Description: Ensure alerts and SLO dashboards are configured for GA
   - Acceptance: SLO dashboards green and alerts tested

3. P3-1103 — Support & onboarding playbooks
   - Estim: 3
   - Owner: PO, Support
   - Description: Prepare onboarding guides and support triage playbooks
   - Acceptance: playbooks available to support team

---

### Sprint 12 (2 semaines) — Post-launch stabilization

1. P3-1201 — Post-launch incident triage & hotfixes
   - Estim: 5
   - Owner: Backend, DevOps, QA
   - Description: Triage production issues, apply hotfixes and communicate status
   - Acceptance: critical incidents resolved and post-mortem created

2. P3-1202 — Model retraining & ops (first cycle)
   - Estim: 8
   - Owner: ML, DevOps
   - Description: Run first retraining cycle using collected feedback and deploy updated models
   - Acceptance: retrained model deployed and monitored

3. P3-1203 — Retrospective & roadmap update
   - Estim: 2
   - Owner: PO, Tech Leads
   - Description: Run project retrospective, update roadmap for next 6 months
   - Acceptance: retro held and roadmap updated

---

## Cross-sprint & technical debt

- P3-TD-01 — Cost governance for ML infra (alerts, budgets) — Estim 3 — Owner: DevOps
- P3-TD-02 — Governance for marketplace content (reputation, anti-fraud) — Estim 5 — Owner: PO
- P3-TD-03 — Accessibility & internationalization (i18n) — Estim 5 — Owner: Frontend, Designer
- P3-TD-04 — Observability for model predictions & drift detection — Estim 5 — Owner: ML, DevOps

---

Fichier créé pour être importé en backlog (GitHub/Jira). Veux-tu que je :

- génère un CSV/JSON prêt à l'import dans GitHub Issues ?
- découpe automatiquement certaines stories en sous-tâches ?
