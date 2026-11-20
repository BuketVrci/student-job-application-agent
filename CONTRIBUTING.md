# Contributing

## Branching

- `main` is protected — never push directly to it.
- Create a feature branch per task: `feat/<short-description>`, `fix/<short-description>`,
  `docs/<short-description>`, `refactor/<short-description>`.
  Examples: `feat/job-scraper`, `feat/cv-tailoring-agent`, `fix/docker-setup`.

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` a new feature
- `fix:` a bug fix
- `docs:` documentation only
- `refactor:` code change that neither fixes a bug nor adds a feature
- `test:` adding or correcting tests
- `chore:` tooling/config/dependency changes

Keep commits small and atomic — one logical change per commit.

## Pull requests

1. Push your branch and open a PR against `main` using the PR template.
2. Describe what changed and how you tested it (the template has a checklist).
3. Make sure CI passes (backend lint/tests, frontend lint/build).
4. Request a review from at least one other team member before merging.

## Code organization

- `backend/app/api/routes/` — one router module per resource (auth, profile, documents, jobs, applications)
- `backend/app/services/` — business logic, grouped by concern (`job_sources/`, `matching/`, `documents/`, `llm/`)
- `backend/app/models/` — SQLAlchemy models (one file per entity)
- `frontend/src/app/` — one route segment per page (Next.js App Router)

Keeping logic in `services/` rather than route handlers makes it easier for multiple people to work on
different modules (e.g. job connectors vs. document generation) without touching the same files.

## Local setup

See the [README](README.md) for Docker and non-Docker setup instructions.
