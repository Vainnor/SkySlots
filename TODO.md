SkySlots TODO
=============

Purpose
-------
High‑level prioritized checklist to reach an MVP and follow‑on improvements.

Immediate (Day 1–7) — Goal: repo bootstrapped + basic event CRUD
---------------------------------------------------------------
- [ ] Create mono‑repo, add bare backend & frontend folders
- [ ] Add infra/docker-compose.yml with services: postgres, redis, minio, backend, worker, frontend
- [ ] Add .env.example
- [ ] Implement SQLModel models for Event, Slot, Booking, User
- [ ] Alembic init + first migration (create core tables)
- [ ] FastAPI skeleton + /health endpoint
- [ ] Next.js skeleton + event list page (static stub)
- [ ] CI skeleton (lint/tests placeholders)

Short term (Weeks 1–4) — Goal: booking flow end‑to‑end
-------------------------------------------------------
- [ ] Events: API endpoints create/list/get
- [ ] Slots: add/edit/delete, CSV import endpoint (preview + apply)
- [ ] Booking endpoint: claim & release with DB constraints
- [ ] Frontend: public event page + BookingModal + optimistic UI
- [ ] Unit tests: core booking conflict logic
- [ ] Docker Compose local end‑to‑end test

Medium (Weeks 5–9) — Goal: polish & integrations
------------------------------------------------
- [ ] iCal export endpoint and caching to MinIO
- [ ] Background scheduler: Celery + reminder task
- [ ] Real‑time updates: WebSocket channels for event updates (backend + frontend)
- [ ] Organizer dashboard (slot bulk edit, booking table)
- [ ] Role-based auth basics (JWT + optional anonymous booking)
- [ ] Add Metabase connection for analytics (docs)

Stabilize & docs (Weeks 10–12)
------------------------------
- [ ] Audit logs for booking actions
- [ ] Tests: integration & E2E (Playwright)
- [ ] GitHub Actions: CI, tests, multi‑arch image builds
- [ ] README, CONTRIBUTING, CODE OF CONDUCT, issue/pr templates
- [ ] Deploy guide (Docker Compose + sample env) and backup notes

Backlog / Nice to have (post‑MVP)
--------------------------------
- [ ] VATSIM OAuth sign‑in & verified pilot linking
- [ ] Waitlist auto‑promotion options
- [ ] Public embed widget for event slots
- [ ] Printable PDF slot sheet generator (WeasyPrint)
- [ ] Templates for airport/position CSVs per VA
- [ ] Integration examples: n8n workflow recipes, Discord bot
- [ ] Multi‑tenant support (multiple VAs with separate namespaces)

Notes
-----
- Prioritize clear error messages for booking conflicts.
- Keep privacy minimal (only store contact email if required).
- Ship small features with good defaults (e.g., reminder times).
