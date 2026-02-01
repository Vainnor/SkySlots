# alembic/versions/0001_initial.py
"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vatsim_id", sa.Integer, nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
    )
    op.create_index(op.f("ix_user_vatsim_id"), "user", ["vatsim_id"], unique=False)

    op.create_table(
        "event",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("start_datetime", sa.DateTime(timezone=False), nullable=False),
        sa.Column("end_datetime", sa.DateTime(timezone=False), nullable=False),
        sa.Column("airport_icao", sa.String(length=10), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
    )
    op.create_index(op.f("ix_event_airport_icao"), "event", ["airport_icao"], unique=False)

    op.create_table(
        "route",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("event.id"), nullable=False),
        sa.Column("origin_icao", sa.String(length=10), nullable=False),
        sa.Column("destination_icao", sa.String(length=10), nullable=False),
        sa.Column("preferred_flightplan", sa.Text, nullable=True),
        sa.Column("frequency_minutes", sa.Integer, nullable=True),
        sa.Column("slot_offset_minutes", sa.Integer, nullable=True),
        sa.Column("slot_duration_minutes", sa.Integer, nullable=True),
        sa.Column("max_slots", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
    )
    op.create_index(op.f("ix_route_event_id"), "route", ["event_id"], unique=False)

    op.create_table(
        "slot",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("event.id"), nullable=False),
        sa.Column("route_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("route.id"), nullable=True),
        sa.Column("position_name", sa.String(length=255), nullable=True),
        sa.Column("position_type", sa.String(length=50), nullable=True),
        sa.Column("callsign_pattern", sa.String(length=64), nullable=True),
        sa.Column("recommended_aircraft", sa.String(length=128), nullable=True),
        sa.Column("scheduled_time", sa.DateTime(timezone=False), nullable=True),
        sa.Column("is_locked", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("order_index", sa.Integer, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
    )
    op.create_index(op.f("ix_slot_event_id"), "slot", ["event_id"], unique=False)
    op.create_index(op.f("ix_slot_route_id"), "slot", ["route_id"], unique=False)
    op.create_index(op.f("ix_slot_scheduled_time"), "slot", ["scheduled_time"], unique=False)

    op.create_table(
        "booking",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slot_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("slot.id"), nullable=False),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("event.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=True),
        sa.Column("pilot_name", sa.String(length=255), nullable=False),
        sa.Column("pilot_callsign", sa.String(length=64), nullable=False),
        sa.Column("pilot_cid", sa.Integer, nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("released_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
    )
    op.create_index(op.f("ix_booking_slot_id"), "booking", ["slot_id"], unique=False)
    op.create_index(op.f("ix_booking_event_id"), "booking", ["event_id"], unique=False)
    op.create_index(op.f("ix_booking_pilot_callsign"), "booking", ["pilot_callsign"], unique=False)
    op.create_index(op.f("ix_booking_pilot_cid"), "booking", ["pilot_cid"], unique=False)

    # audit log
    op.create_table(
        "auditlog",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=True),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("event.id"), nullable=True),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("payload", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
    )

    # PostgreSQL partial unique index: only one claimed booking per slot
    op.create_index(
        "uq_booking_slot_claimed",
        "booking",
        ["slot_id"],
        unique=True,
        postgresql_where=sa.text("status = 'claimed'"),
    )

    # PostgreSQL partial unique index: only one claimed slot per (event, pilot_cid)
    op.create_index(
        "uq_booking_event_pilot_claimed",
        "booking",
        ["event_id", "pilot_cid"],
        unique=True,
        postgresql_where=sa.text("status = 'claimed' AND pilot_cid IS NOT NULL"),
    )

    # optional: unique constraint on vatsim_id if you want
    op.create_index("uq_user_vatsim_id", "user", ["vatsim_id"], unique=True)


def downgrade():
    op.drop_index("uq_user_vatsim_id", table_name="user")
    op.drop_index("uq_booking_event_pilot_claimed", table_name="booking")
    op.drop_index("uq_booking_slot_claimed", table_name="booking")
    op.drop_table("auditlog")
    op.drop_table("booking")
    op.drop_index(op.f("ix_slot_scheduled_time"), table_name="slot")
    op.drop_index(op.f("ix_slot_route_id"), table_name="slot")
    op.drop_index(op.f("ix_slot_event_id"), table_name="slot")
    op.drop_table("slot")
    op.drop_index(op.f("ix_route_event_id"), table_name="route")
    op.drop_table("route")
    op.drop_index(op.f("ix_event_airport_icao"), table_name="event")
    op.drop_table("event")
    op.drop_index(op.f("ix_user_vatsim_id"), table_name="user")
    op.drop_table("user")