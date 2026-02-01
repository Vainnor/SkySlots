Contributing to SkySlots
========================

Thanks for your interest! This guide explains how to contribute code, file issues,
and propose changes.

1) Code of conduct
------------------
Respectful behavior required. Follow the CODE_OF_CONDUCT in repo.

2) Development environment
--------------------------
Prereqs:
- Docker & Docker Compose
- Node 16+ (for frontend dev)
- Python 3.10+ (for backend dev)
- Make (optional) for convenience scripts

Quickstart (local)
- Copy .env.example -> infra/.env and edit values if needed
- From repo root:
  docker compose -f infra/docker-compose.yml up --build

Backend
- Virtualenv optional; dependencies in pyproject.toml or requirements.txt
- Run migrations:
  (inside backend container) alembic upgrade head
- Start dev server:
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Frontend
- Install deps:
  cd frontend && pnpm install | npm install
- Start dev:
  pnpm dev | npm run dev

3) Code style
-------------
Python:
- ruff for linting, black for formatting, isort for imports.
- Tests: pytest

TypeScript / React:
- ESLint + Prettier. Follow the project ESLint rules.

Commit messages
- Use concise messages. Prefer Conventional Commits (feat/, fix/, docs/).
- Squash feature branch commits when merging unless requested otherwise.

4) Branches & PRs
-----------------
- Create a feature branch off main: feature/<short-desc>
- Open a PR with description, screenshots (if UI), and link to issue.
- Ensure CI passes (lint + tests) before requesting review.

5) Running tests
----------------
- Backend:
  docker compose exec backend pytest
- Frontend:
  cd frontend && pnpm test

6) Issues & feature requests
----------------------------
- Use the issue templates.
- For feature requests: include user story, acceptance criteria, and mockups if possible.

7) Adding new dependencies
--------------------------
- New Python libs -> add to pyproject.toml/requirements and update Dockerfile.
- New Node libs -> add to package.json.
- Keep dependencies minimal.

8) Security fixes / sensitive issues
-----------------------------------
- Report sensitive/security issues privately (contact info in repo settings)
- Do not open a public issue for security vulnerabilities.

9) Help & contact
-----------------
If you have questions, open a discussion or reach out via the repo issues.
