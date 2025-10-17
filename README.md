# SpecFlow - tooling and scripts

[![CI](https://github.com/mrouanet31/specflow/actions/workflows/ci.yml/badge.svg)](https://github.com/mrouanet31/specflow/actions/workflows/ci.yml)
[![Codecov](https://img.shields.io/codecov/c/github/mrouanet31/specflow.svg)](https://codecov.io/gh/mrouanet31/specflow)
[![License](https://img.shields.io/github/license/mrouanet31/specflow.svg)](https://github.com/mrouanet31/specflow/blob/main/LICENSE)

This repository contains implementation plans, sprint backlogs and helper scripts for importing backlog items into GitHub issues.

See `scripts/README.md` for the GitHub Issue Importer usage and examples.

## Coverage policy

The CI enforces a minimum coverage threshold of 80%. If coverage drops below this threshold the build will fail. To change the threshold, edit `.github/workflows/ci.yml` and update the `--cov-fail-under` value.

## Next steps to raise coverage

Current total coverage is ~76%. To reach 80% we should add targeted tests around the untested branches in `scripts/github_issue_importer.py` (network error handling, label/milestone failure paths, parsing edge-cases). I can create a short plan and a small set of tests to raise coverage to 80% if you want.

## Onboarding & local dev

This repo now contains a minimal monorepo skeleton as part of INIT-001 (see `INIT-001-plan.md`). To get started locally:

```bash
git clone <repo>
cd <repo>
# Frontend (Angular placeholder)
cd frontend && npm ci && npm run build
# Backend (Spring Boot)
cd backend && mvn -q -DskipTests package
```

The GitHub Actions CI runs a minimal build for both frontend and backend. The full plan for INIT-001 is in `INIT-001-plan.md`.

Onboarding notes
- The feature branch `feature/INIT-001-initialize-monorepo` contains the initial scaffolding. Open a PR with `INIT-001-plan.md` in the description to start the review.
