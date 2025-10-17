## Phase 2 — Growth (3 mois) : Plan d'implémentation

## Objectif

Monétiser et solidifier le produit après le MVP en livrant des fonctionnalités à forte valeur pour les utilisateurs avancés :

- Technical Plan Builder (génération de plans techniques)
- Quality Assurance Dashboard (vérification spec→implémentation)
- Git Integration Hub (sync repos & CI integration)
- SpecGPT (alpha) — assistant IA contextuel
- Marketplace (structure et catalogue initial)

## Hypothèses

- Base MVP déployée en staging et validée (Phase 1 terminée)
- Équipe : 2 backend, 2 frontend, 1 designer, 0.5 ML/IA engineer, 0.5 DevOps
- Accès à services IA (API OpenAI/Anthropic) ou possibilité de démarrer en mode local/stub
- Budget pour infra additionnelle (indexation, Elasticsearch, storage)

## Calendrier & cadence

- Durée : 3 mois — 6 sprints de 2 semaines
- Orientation : paralléliser plusieurs epics en conservant une priorité PO

## Rôles clés

- PO : priorisation et acceptance
- Tech Lead Backend & Frontend
- IA/ML Engineer : prototypage SpecGPT, intégration modèle
- DevOps : infra search, scalable ingestion, monitoring
- Designer : flows Marketplace, composants UI
- QA : tests E2E + intégration IA

## Définition de Done (Phase 2)

Pour chaque delivery :

- API documentée (OpenAPI) et testable
- UI intégrée avec design system et accessible
- Tests unitaires + intégration et scénarios E2E critiques verts
- Déployée en staging et validée par PO

## Sprint-by-sprint (haut niveau)

Sprint 1 (2 semaines) — Foundations & Discovery

- Objectifs : discovery technique pour SpecGPT et Technical Plan Builder, infra search
- Tâches :
  - Audit MVP pour points d'intégration (webhooks, API, events)
  - Provisionner Elasticsearch / vector DB (Pinecone / Milvus / OpenSearch) pour indexation specs
  - Définir schema d'indexation (specs, versions, metadata)
  - Prototyper SpecGPT pipeline (ingestion → embedding → retrieval)
  - Design initial Marketplace (catalog model, pricing model, contribution flow)
- Critères d'acceptation : PoC embedding + retrieval, index opérationnel en staging

Sprint 2 (2 semaines) — Technical Plan Builder (MVP)

- Objectifs : livrer un builder capable de générer plans techniques structurés depuis une spec
- Tâches :
  - Backend : endpoint /api/plan-builder (POST spec -> PlanDraft)
  - Engine : rule-based generator + template engine (mustache/liquid) pour MVP
  - Frontend : UI wizard (inputs, stack selector, output preview), export JSON/MD
  - Tests : sample specs -> generate plans, validations schema
- Critères d'acceptation : génération cohérente d'au moins 3 templates de plan, UI pour reviewer

Sprint 3 (2 semaines) — Quality Assurance Dashboard

- Objectifs : dashboard montrant conformité spec→implémentation et metrics QA
- Tâches :
  - Data model : mapping spec -> implementations (coverage, tests linked)
  - Backend : endpoints pour calculer Spec Completion Score, Risk Heat Map
  - Frontend : dashboard widgets (coverage, open issues, test coverage vs acceptance)
  - Integrations : pipelines CI pour remonter test results, simple rules engine
- Critères d'acceptation : dashboard remplit avec données staging (test coverage, checklist)

Sprint 4 (2 semaines) — Git Integration Hub

- Objectifs : lier specs aux repos, créer PRs depuis tasks, webhook handling
- Tâches :
  - OAuth connectors for GitHub/GitLab/Bitbucket
  - Sync engine : map spec -> repo, create branch + PR template
  - Webhooks listener : events -> update spec/task status
  - UI : onboarding repo, auth flow, repo linking
- Critères d'acceptation : flow end-to-end pour créer PR depuis une tâche (staging)

Sprint 5 (2 semaines) — SpecGPT alpha (IA) & Integrations

- Objectifs : livrer une alpha SpecGPT (assistant contextuel) en mode limité
- Tâches :
  - IA infra : hooking to model provider (OpenAI/Anthropic) + rate-limiter
  - Context builder : retrieve relevant specs (RAG) + prompt templates
  - Features alpha : generate section suggestions, ambiguity detection, spec summarization
  - Safety & governance : allow manual review, usage logs, simple filtering
- Critères d'acceptation : assistant capable de proposer suggestions utiles sur 80% des specs testées en staging

Sprint 6 (2 semaines) — Marketplace (structure) & Polish

- Objectifs : lancer la structure marketplace (catalog, contribution flow) et finaliser intégrations
- Tâches :
  - Backend : catalog model, listing API, basic billing stubs (or placeholders)
  - Frontend : marketplace browsing, upload spec template, fork/clone flow
  - Legal & compliance: TOS skeleton, content moderation rules
  - Polish : docs, demo flows, bug fixes, performance tuning
- Critères d'acceptation : marketplace navigable, capacité à upload/fork template, PO validation

## Epics & stories prioritaires

- EPIC: SpecGPT

  - Story: ingestion pipeline (embeddings + retrieval)
  - Story: prompt templates library
  - Story: UI assistant (inline suggestions)
  - Story: logging & feedback loop

- EPIC: Technical Plan Builder

  - Story: template engine
  - Story: stack selector & biases mitigation
  - Story: export to tasks (auto-generation)

- EPIC: QA Dashboard

  - Story: rules engine for acceptance checks
  - Story: CI integration (test results ingestion)
  - Story: visualization widgets

- EPIC: Git Integration Hub

  - Story: OAuth connectors
  - Story: PR creation & branch naming rules
  - Story: bidirectional sync

- EPIC: Marketplace
  - Story: catalog model
  - Story: contribution flow & moderation
  - Story: rating & reviews

## Non-functional requirements

- Latency : RAG retrieval < 300ms median for small embeddings store
- Security : secrets management, least privilege for repo access
- Scalability : vector DB scalable, async ingestion
- Privacy : PII detection and redaction in ingestion

## Data & IA considerations

- Privacy-by-design : opt-in ingestion of company specs for model fine-tuning
- Relevance pipeline : embeddings (OpenAI/OPAQ/FAISS) + hybrid retrieval (semantic + keyword)
- Human-in-the-loop : always require manual acceptance for changes suggested by SpecGPT
- Cost control : caching frequent retrievals, paying attention to tokens usage

## CI/CD & Release

- Feature toggles pour SpecGPT and Marketplace
- Canary deploys pour nouvelles integrations (Git hub connectors)
- CI pipelines : unit + integration + E2E for all new features

## Monitoring & Observability

- Metrics : suggestions accepted rate, RAG latency, marketplace uploads, PR creation success
- Alerts : failure rate of retrieval, IA provider errors, oauth failures

## Risques majeurs & mitigations

- Risque : coût IA élevé
  - Mitigation : démarrer en mode stubs / light-weight models, batching et caching
- Risque : intégration Git complexe (permissions)
  - Mitigation : commencer par scope limité (repos privés autorisés par admin), UX d'onboarding clair
- Risque : modération contenu marketplace
  - Mitigation : règles automatiques + revue manuelle préalable pour premiers uploads
- Risque : qualité des plans générés faible
  - Mitigation : commencer par rule-based templates + human review, mesurer accepted rate

## Critères de succès Phase 2

- Technical Plan Builder generant plans exploitables pour 3 templates communs
- QA Dashboard remontant metrics clés et aidant à détecter 80% des écarts simples
- Git Integration Hub capable de créer PRs et synchroniser statut (staging)
- SpecGPT alpha offrant suggestions utiles (mesuré par taux d'acceptation utilisateur >= 40%)
- Marketplace structure en place (catalog + contribution flow) et 10 templates initiales

## Livrables fin de Phase 2

- Services : Plan Builder API, QA Dashboard API, Git Integration microservice
- SpecGPT alpha : pipelines RAG + UI assistant
- Marketplace : catalog API + UI, basic moderation
- Infra : vector DB / Elasticsearch provisionné et indexé
- Documentation : runbooks, API OpenAPI, how-to pour contributors

## Suivi & gouvernance

- Métriques hebdo pour PO & Stakeholders
- Réunions de gouvernance mensuelles pour priorisation marketplace
- Feedback loop IA : collecte annotations utilisateurs pour amélioration modèles

## Prochaines étapes immédiates

1. Validation PO & priorisation des 6 sprints
2. Provisionnement vector DB / search et PoC retrieval
3. Kickoff SpecGPT alpha (small scope)

## Annexe : idées rapides & extensions

- Extension : export de plans en issues/epics vers Jira/GH Projects
- Extension : intégration CI pour évaluer diff tests sur PRs générés
- Extension : marketplace premium (templates payants) et analytics auteurs

---

Fichier créé pour servir de feuille de route exécutable pour Phase 2 — Growth.
