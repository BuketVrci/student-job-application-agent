# Student Job Application Agent

An AI-powered agent that helps university students in Germany find relevant **Werkstudent** (working student)
and **Praktikum** (internship) positions, tailor application documents to each job, and track applications —
always with explicit human approval before anything is sent.

## Features (MVP roadmap)

- Student profile & base CV upload (PDF/DOCX)
- Automated job discovery via legal, public APIs (Arbeitnow, Adzuna), with modular connectors for more sources
- AI-tailored CVs and cover letters (German/English), previewable and editable before export
- Human-in-the-loop Approve / Edit / Reject workflow
- Application tracker: `Found → Draft Ready → Approved → Applied → Interview / Rejected`

See [docs/architecture.md](docs/architecture.md) for the full architecture and milestone plan.

## Tech stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Database:** PostgreSQL 16 (via Docker only — no separate SQLite path)
- **AI layer:** Provider-agnostic LLM interface; default is local **Ollama** (no API key needed), with
  OpenAI / Anthropic / Gemini adapters selectable via `.env`
- **Job sources:** Arbeitnow (no key required), Adzuna (free developer API key)

## Getting started (any OS: Windows, macOS, Linux)

### Option A — Docker (recommended, one command)

Requires [Docker](https://docs.docker.com/get-docker/) and Docker Compose (bundled with Docker Desktop).

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (health check at `/health`)
- Postgres: localhost:5432
- Ollama: localhost:11434 (first run will need to pull a model, e.g. `docker compose exec ollama ollama pull llama3.1:8b`)

Stop with `docker compose down` (add `-v` to also wipe the database/model volumes).

### Option B — Local development without Docker

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

You'll need a local PostgreSQL instance and to set `DATABASE_URL` in `backend/.env` accordingly (or point
`OLLAMA_PROVIDER`/API keys at a provider that doesn't need the bundled Ollama container).

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

Copy `.env.example` to `.env` and fill in secrets as needed. Never commit `.env`. See the file for all
available settings (database, JWT secret, LLM provider selection, job source API keys).

## Running tests / linting

```bash
# Backend
cd backend && pip install -r requirements.txt && ruff check . && pytest

# Frontend
cd frontend && npm install && npm run lint && npm run build
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit conventions, and the PR process.
