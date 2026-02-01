SkySlots — Architecture Overview
================================

Purpose
-------
This document gives a high‑level architecture of SkySlots, explains core components,
data flows (booking & realtime), background jobs, storage/backup, and CI/CD.
It’s intended for contributors and operators (home‑lab / single host).

High-level components
---------------------
- Frontend (Next.js + TypeScript + MUI)
  - Public event pages, organizer dashboard, booking modal, WebSocket client.
- Backend API (FastAPI + SQLModel + Alembic)
  - REST endpoints, WebSocket endpoints, booking business logic, auth.
- Database (PostgreSQL)
  - Persistent storage for events, slots, bookings, users, audit logs.
- Redis
  - Celery broker/result backend and pub/sub for realtime notifications.
- Celery workers
  - Background jobs: reminders, waitlist promotion, cleanup, exports.
- Object Storage (MinIO)
  - Store generated artifacts: iCal/.ics files, exported CSVs, generated PDFs, screenshots.
- Reverse proxy / router (Traefik suggested)
  - HTTPS termination (Let's Encrypt), subdomain routing (frontend, docs, api).
- Optional extras:
  - n8n for notification workflows
  - Metabase for analytics
  - Sentry or similar for errors

Deployment model
----------------
- Single-host Docker Compose for MVP.
- Services run as containers on a single host; Traefik routes subdomains to services.
- CI/CD: GitHub Actions builds images (multi‑arch if required) and pushes to registry; deploy via SSH or run docker compose pull + up on host.

Data model (core)
-----------------
- events (id, title, description, start_datetime, end_datetime,
  airport_icao, timezone, organizer_id, created_at)
- slots (id, event_id, position_name, position_type, callsign_pattern,
  is_locked, order_index, notes)
- bookings (id, slot_id, user_id, pilot_name, pilot_callsign, email,
  status, claimed_at, released_at, notes)
- users (id, vatsim_id, name, email, role, created_at)
- audit_logs (id, event_id, user_id, action_type, payload, created_at)

Booking flow (end‑to‑end)
-------------------------
1. User clicks "Claim" on slot on frontend.
2. Frontend sends POST /api/slots/:id/book {pilot_name, pilot_callsign, email, notes}.
3. Backend booking service:
   - Begin DB transaction.
   - Option A (recommended): attempt INSERT into bookings with constraint
     that only one booking with status='claimed' can exist for slot_id.
     If unique constraint violation -> return 409 with reason (already claimed).
   - Also enforce unique partial index to prevent same callsign claiming
     multiple slots in same event:
     UNIQUE(event_id, lower(pilot_callsign)) WHERE status='claimed'
   - Commit transaction.
4. Backend publishes "slot.updated" message to Redis pub/sub channel for event.
5. Celery task optionally enqueued (notify webhooks / n8n).
6. Frontend receives WebSocket event and updates UI in real time.

Concurrency & correctness
-------------------------
- Use DB transactions and unique constraints as the primary guard.
- For stronger control, SELECT FOR UPDATE on slot row before checking and inserting,
  but inserting with constraints is usually sufficient and scales well.
- Return clear HTTP status codes:
  - 201/200 success
  - 409 conflict (include human-readable reason)
  - 422 validation

Realtime design
---------------
- Backend exposes WebSocket endpoint (/ws/events/{event_id}) for subscribers.
- On booking state change, backend publishes event to Redis channel (e.g. "event:<id>").
- A lightweight broadcaster (inside backend process or separate) subscribes to Redis
  and forwards updates to connected WebSocket clients.
- Fall back: polling with React Query (short interval) for resilience.

iCal / Export flow
------------------
- User requests /api/events/:id/calendar.ics
- Backend generates .ics (python-ics), stores object in MinIO, and returns presigned URL
  (or streams .ics directly on first request and caches in MinIO for subsequent requests).
- Celery task can pre-generate caches when event is created/updated.

Background jobs (Celery)
------------------------
- Reminder emails / Discord messages:
  - Configurable reminder times (e.g., 24h, 1h), enqueued at event creation or scheduled.
- Waitlist promotion:
  - Promote next in waitlist when a slot becomes available.
- Cleanup job:
  - Remove stale temporary holds.
- Export generation (CSV/PDF) for admin requests.

Storage & backups
-----------------
- Postgres: schedule regular pg_dump snapshots; keep off‑site copies if possible.
- MinIO: use `mc` to mirror to remote bucket (S3/B2) or backup dumps.
- Redis: ephemeral; persist if desired via RDB/AOF.
- Suggested backup jobs run via cron container or external scheduler.

Security & privacy
------------------
- Minimal PII: store only necessary contact info (email for reminders).
- Rate limit booking endpoints (per-IP and per-slot) to mitigate spam.
- Allow anonymous bookings (recommended) but consider email confirmation option.
- HTTPS required in production (Traefik + Let's Encrypt).
- Provide data export/delete endpoints to comply with privacy preferences.

Observability & monitoring
--------------------------
- Structured logs (JSON), expose /health and /metrics endpoints.
- Integrate Sentry for errors (optional).
- Metrics: Prometheus + Grafana (optional) or external monitoring.

CI/CD
-----
- GitHub Actions workflows:
  - ci.yml: lint (ruff/black/eslint), unit tests (pytest, jest), build preview images.
  - publish.yml: build & push multi‑arch images with buildx, then deploy trigger.
- Deploy options:
  - SSH action that runs `docker compose pull && docker compose up -d`.
  - Or push images to registry and use a small deploy runner on host.

Operational notes
-----------------
- Provide clear migration path (Alembic) and seed fixture generator.
- Use feature flags for major new behavior.
- Keep the simple UX: minimal booking form and clear conflict messages.

Appendix: key DB indices / constraints
- Unique constraint on bookings table: (slot_id) WHERE status='claimed'
- Partial unique index on bookings: (event_id, lower(pilot_callsign)) WHERE status='claimed'
- Index events.start_datetime, slots.event_id, bookings.slot_id

Change log
----------
- Keep this file updated when architecture decisions change.
