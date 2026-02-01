import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

# add backend package to sys.path so we can import app.models
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "backend"))
sys.path.insert(0, BACKEND_PATH)

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Use DATABASE_URL env var if present, otherwise fallback to alembic.ini value
db_url = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
if not db_url:
    raise RuntimeError("DATABASE_URL not set and sqlalchemy.url not configured in alembic.ini")
config.set_main_option("sqlalchemy.url", db_url)

# Import SQLModel metadata by importing your models module.
# Ensure backend/app/models.py registers models against SQLModel.metadata
try:
    # this should import backend/app/models.py (package import path: app.models)
    import app.models  # noqa: F401
except Exception as e:  # pragma: no cover
    raise

from sqlmodel import SQLModel, create_engine

target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(db_url, pool_pre_ping=True)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()