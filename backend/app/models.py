# backend/app/models.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


def now():
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    vatsim_id: Optional[int] = Field(default=None, index=True)
    name: str
    email: str
    role: str = Field(default="pilot")  # pilot, organizer, admin
    created_at: datetime = Field(default_factory=now)


class Event(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    airport_icao: Optional[str] = Field(default=None, index=True)
    timezone: str = Field(default="UTC")
    created_at: datetime = Field(default_factory=now)

    routes: List["Route"] = Relationship(back_populates="event")
    slots: List["Slot"] = Relationship(back_populates="event")


class Route(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="event.id", index=True)
    origin_icao: str
    destination_icao: str
    preferred_flightplan: Optional[str] = None
    frequency_minutes: Optional[int] = None  # e.g., 15
    slot_offset_minutes: Optional[int] = Field(default=0)
    slot_duration_minutes: Optional[int] = Field(default=60)
    max_slots: Optional[int] = None
    created_at: datetime = Field(default_factory=now)

    event: Event = Relationship(back_populates="routes")
    slots: List["Slot"] = Relationship(back_populates="route")


class Slot(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="event.id", index=True)
    route_id: Optional[UUID] = Field(default=None, foreign_key="route.id", index=True)
    position_name: Optional[str] = None
    position_type: Optional[str] = None
    callsign_pattern: Optional[str] = None
    recommended_aircraft: Optional[str] = None
    scheduled_time: Optional[datetime] = Field(default=None, index=True)
    is_locked: bool = Field(default=False)
    order_index: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=now)

    event: Event = Relationship(back_populates="slots")
    route: Optional[Route] = Relationship(back_populates="slots")
    bookings: List["Booking"] = Relationship(back_populates="slot")


class Booking(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    slot_id: UUID = Field(foreign_key="slot.id", index=True)
    event_id: UUID = Field(foreign_key="event.id", index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", index=True)

    pilot_name: str
    pilot_callsign: str = Field(index=True)
    pilot_cid: Optional[int] = Field(default=None, index=True)
    email: Optional[str] = None

    status: str = Field(default="claimed")  # claimed, waitlist, cancelled, released
    claimed_at: datetime = Field(default_factory=now)
    released_at: Optional[datetime] = None
    notes: Optional[str] = None

    slot: Slot = Relationship(back_populates="bookings")


class AuditLog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", index=True)
    event_id: Optional[UUID] = Field(default=None, foreign_key="event.id", index=True)
    action: str
    payload: Optional[str] = None  # JSON string
    created_at: datetime = Field(default_factory=now)