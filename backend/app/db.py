# backend/app/db.py
import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")  # infra .env provides this

# SQLModel/SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Session factory for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session