SkySlots — VATSIM Event Planner & Slot Manager
=============================================

One‑line: Self‑hosted event & slot manager for VATSIM communities and virtual
airlines.

Stack
- Frontend: Next.js (TypeScript) + MUI
- Backend: FastAPI + SQLModel + Alembic
- DB: PostgreSQL
- Background: Redis + Celery
- Object storage: MinIO
- Realtime: WebSockets via FastAPI
- Deploy: Docker Compose
- CI/CD: GitHub Actions

Quickstart (dev)
1. Copy env: infra/.env.example -> infra/.env
2. docker compose -f infra/docker-compose.yml up --build
3. Backend: http://localhost:8000, Frontend: http://localhost:3000

Goals / MVP
- Create/manage events and slots
- Claim/release slots with conflict checks
- Public event page + booking modal
- iCal export + reminders (via Celery)

See docs/ for architecture, API, and roadmap.

Contributing
------------
See CONTRIBUTING.md

License
-------
GNU GENERAL PUBLIC LICENSE
