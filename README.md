# JARVIS-OS (Phase 1 Foundation)

JARVIS-OS is a production-ready foundation for an AI Operating System built around a **multi-agent backend**, **persistent memory**, and a **dark-themed operator UI**.

## Tech Stack

- **Backend**: FastAPI (async), SQLAlchemy 2.0, JWT auth
- **Frontend**: React 18 + Tailwind CSS (dark + electric blue theme)
- **Relational DB**: PostgreSQL
- **Vector Memory**: ChromaDB
- **Task Queue**: Celery + Redis
- **AI Provider**: Anthropic Claude API

## Project Structure

```text
.
├── backend/
│   ├── __init__.py
│   ├── auth.py
│   ├── celery_app.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── agents.py
│       ├── chat.py
│       ├── memory.py
│       └── users.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── index.css
│       ├── main.jsx
│       └── pages/
│           ├── ChatPage.jsx
│           ├── DashboardPage.jsx
│           └── SettingsPage.jsx
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── browser_agent.py
│   ├── calendar_agent.py
│   ├── email_agent.py
│   ├── job_agent.py
│   └── research_agent.py
├── memory/
│   ├── __init__.py
│   ├── summarizer.py
│   ├── user_profile.py
│   └── vector_store.py
├── tools/
│   ├── __init__.py
│   ├── browser_tool.py
│   ├── calendar_tool.py
│   ├── file_manager.py
│   ├── gmail_tool.py
│   ├── tool_registry.py
│   └── web_search.py
├── orchestrator/
│   ├── __init__.py
│   ├── coordinator.py
│   └── planner.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── tests/
│   ├── __init__.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_health.py
│   └── unit/
│       ├── __init__.py
│       └── test_planner.py
├── .env.example
├── .gitignore
├── docker-compose.yml
└── requirements.txt
```

## Architecture Overview

### 1) Backend (`/backend`)

- **`main.py`**: FastAPI entry point, CORS, startup lifecycle, router registration
- **`auth.py`**: Password hashing (bcrypt), JWT token generation/validation, current-user dependency
- **`database.py`**: SQLAlchemy 2.0 async engine + session lifecycle
- **`models.py`**: Core relational entities (`User`, `Conversation`, `Message`, `MemoryEntry`)
- **`schemas.py`**: API contracts and validation
- **`routers/`**:
  - `users.py`: register/login/me
  - `chat.py`: Claude-backed chat endpoint + orchestrator routing
  - `memory.py`: relational memory read/write endpoints
  - `agents.py`: list and execute internal agents

### 2) Agent Layer (`/agents`)

Each agent inherits from `BaseAgent` and exposes an async `run(task: str)` entry point.  
Phase 1 includes:

- Email
- Calendar
- Research
- Browser
- Job

This keeps orchestration pluggable while allowing specialized behavior per domain.

### 3) Memory Layer (`/memory`)

- **`vector_store.py`**: ChromaDB wrapper for semantic retrieval
- **`user_profile.py`**: relational profile preferences store (PostgreSQL)
- **`summarizer.py`**: summarization utility for recalled memory chunks

This creates dual-memory behavior:

1. **Structured memory** in PostgreSQL
2. **Semantic memory** in ChromaDB

### 4) Tooling Layer (`/tools`)

Centralized adapters for external capabilities:

- Gmail
- Calendar
- Browser
- Web search
- File management

`tool_registry.py` provides a single lookup interface for orchestrator/agents.

### 5) Orchestration Layer (`/orchestrator`)

- **`planner.py`**: intent routing heuristics
- **`coordinator.py`**: multi-agent coordination entry point

This is the central decision layer that maps user input to the right agent flow.

### 6) Frontend (`/frontend`)

React + Tailwind app with:

- **Dashboard** (system status cards)
- **Chat** (operator console style UI)
- **Settings** (runtime/provider visibility)

Theme: dark (`black`) + electric blue accents.

### 7) Config Layer (`/config`)

- `settings.py` uses `pydantic-settings` to load environment variables safely.

### 8) Testing (`/tests`)

- `tests/unit`: logic-level tests (planner routing)
- `tests/integration`: API-level tests (health endpoint)

## Quick Start

### 1. Infrastructure

```bash
docker compose up -d
```

### 2. Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment

```bash
cp .env.example .env
```

Set at minimum:

- `SECRET_KEY`
- `DATABASE_URL`
- `ANTHROPIC_API_KEY`

### 4. Run API

```bash
uvicorn backend.main:app --reload
```

### 5. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

### 6. Optional Celery Worker

```bash
celery -A backend.celery_app.celery_app worker --loglevel=info
```

## API Surface (Phase 1)

- `GET /healthz`
- `POST /api/v1/users/register`
- `POST /api/v1/users/login`
- `GET /api/v1/users/me`
- `POST /api/v1/chat/`
- `POST /api/v1/memory/`
- `GET /api/v1/memory/{key}`
- `GET /api/v1/agents/`
- `POST /api/v1/agents/run`

## Production Notes for Next Phases

- Replace startup table creation with Alembic migrations
- Add OAuth providers and RBAC
- Add background workflows for agent execution via Celery tasks
- Add observability: OpenTelemetry, structured logs, metrics
- Add model fallback strategy and prompt versioning
- Harden tool adapters with real provider SDK integrations
