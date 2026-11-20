# Architecture

## Tech stack

| Layer | Choice | Notes |
|---|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic | REST API + AI agent orchestration |
| Auth | Custom JWT (passlib + python-jose) | Multi-user; no third-party auth framework |
| Database | PostgreSQL 16, Docker only | One schema for every environment |
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS | |
| AI layer | Provider-agnostic `LLMProvider` interface, default `ollama`, pluggable `openai`/`anthropic`/`gemini` via `LLM_PROVIDER` env var | Ollama runs as its own Docker service so the whole stack works with zero API keys |
| Job sources | `JobSource` interface; `arbeitnow` (no key) + `adzuna` (free key) | Both are legal/public APIs |
| Document parsing/export | `pdfplumber` / `python-docx` (parse), `weasyprint` (PDF export) + `python-docx` (DOCX export) | |
| Scheduling | APScheduler inside the FastAPI process | Avoids Celery/Redis for MVP |

## Database schema

Five tables, deliberately not over-normalized for the MVP:

- **users** — id, email (unique), hashed_password, full_name, created_at
- **student_profiles** (1:1 with users) — field_of_study, target_role_type
  (`werkstudent`/`praktikum`/`either`), preferred_cities (jsonb), remote_ok, language_preference
  (`de`/`en`/`both`), skills (jsonb array), base_cv_document_id → documents, updated_at
- **documents** — user_id, type (`base_cv`/`tailored_cv`/`cover_letter`), language, file_path,
  original_filename, content_text (extracted text), created_at
- **jobs** — external_id + source (unique pair), title, company, location, remote, description, url,
  posted_at, raw_json, fetched_at
- **applications** (combined match + tracker record) — user_id, job_id, status
  (`found`/`draft_ready`/`approved`/`applied`/`interview`/`rejected`), match_score, match_reasoning,
  cv_document_id, cover_letter_document_id, notes, timestamps

## Folder structure

```
student-job-application-agent/
├── README.md  CONTRIBUTING.md  .gitignore  .env.example  docker-compose.yml
├── backend/
│   ├── Dockerfile  requirements.txt  alembic.ini  alembic/versions/
│   └── app/
│       ├── main.py
│       ├── core/        # config.py, security.py
│       ├── db/          # base.py, session.py
│       ├── models/      # user.py, profile.py, document.py, job.py, application.py
│       ├── schemas/
│       ├── api/routes/  # auth.py, profile.py, documents.py, jobs.py, applications.py
│       ├── services/
│       │   ├── job_sources/   # base.py, arbeitnow.py, adzuna.py
│       │   ├── matching/      # scorer.py
│       │   ├── documents/     # cv_parser.py, cv_generator.py, cover_letter_generator.py
│       │   └── llm/           # base.py, ollama_provider.py, openai_provider.py, anthropic_provider.py, gemini_provider.py
│       └── tests/
├── frontend/
│   ├── Dockerfile  package.json  next.config.mjs  tailwind.config.ts
│   └── src/
│       ├── app/   # login/ dashboard/ profile/ jobs/ documents/ tracker/
│       ├── components/
│       └── lib/api.ts
└── docs/architecture.md
```

## MVP milestones (each its own branch + PR)

1. **M0 — Scaffolding** *(this PR)*: Docker Compose (backend/frontend/postgres/ollama), FastAPI `/health`,
   Next.js shell, full DB schema + initial Alembic migration, CI, README/CONTRIBUTING, `.env.example`
2. **M1 — Auth & Profile**: signup/login (JWT), profile CRUD, CV upload + text extraction
3. **M2 — Job Discovery**: Arbeitnow + Adzuna connectors, fetch endpoint + scheduler, jobs browse UI
4. **M3 — Matching Engine**: scoring + LLM reasoning, ranked jobs UI
5. **M4 — Document Tailoring**: LLM CV/cover-letter generation (EN/DE), PDF/DOCX export, preview/edit
6. **M5 — HITL Dashboard & Tracker**: Approve/Edit/Reject workflow, full tracker UI
7. **M6 — Application Assist**: email drafts, prefilled data export, redirect flow
8. **M7 — Polish**: test coverage, deployment docs, security hardening pass
