# Contributing to Specflow

This document describes the team conventions for contributing to this repository. It is intended to keep the codebase consistent and the review process efficient.

## Branch strategy

- Use feature branches prefixed with the issue id: `feature/INIT-123-description`.
- Use `main` as the protected production branch. Create PRs from feature branches into `main`.
- Small fixes: `fix/<short-desc>`; experiments: `exp/<short-desc>`.

## Commit messages

Follow the Conventional Commits style (https://www.conventionalcommits.org):

Format: `type(scope?): subject`

Examples:
- `feat(auth): add refresh token endpoint`
- `fix(ci): use gradle wrapper for backend build`
- `chore: update README`

Types commonly used:
- `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.

Keep the subject short (<= 72 chars). Add a body when necessary to explain the why.

## Formatting & linting

- Java: use `google-java-format` or the project's formatter (see `backend/` configuration).
- TypeScript/Angular: use `prettier` and `eslint` with Angular recommended rules.
- Run linters and formatters before pushing; CI runs checks on PRs.

## Tests

- Add unit tests for new logic. Backend uses JUnit 5 and Spring Boot test slices. Frontend uses Karma/Jasmine (unit) and Cypress (E2E) for major flows.
- CI requires tests to pass; coverage target enforced by CI is 80%.

## Pull requests

- Use the PR template when opening a PR.
- Include a short description, related issue (e.g. `Closes #123`), testing instructions, and checklist.
- Self-review before requesting reviewers. Add reviewers as appropriate.

### PR checklist (example)
- [ ] Title follows `type(scope?): subject` convention
- [ ] Tests added / updated
- [ ] CI green
- [ ] Docs updated (if applicable)

## Code review

- Prefer small, focused PRs (≤ 300 lines changed) for easier review.
- Use line comments for implementation questions; use review summary for high-level feedback.

## Local development

- Backend: `cd backend && ./gradlew bootRun`
- Frontend: `cd frontend && npm ci && npm run build`

## Security & Secrets

- Never commit secrets to the repo. Use GitHub Actions secrets or an external vault.

## Thanks

Thank you for contributing! If you have suggestions to improve these guidelines, open a PR or an issue.
