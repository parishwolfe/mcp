"""Database configuration and session management for the FastAPI store backend."""
from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DEFAULT_DATABASE_URL = "postgresql+psycopg2://mcp_user:mcp_password@localhost:5432/mcp_store"


@lru_cache
def get_database_url() -> str:
    """Return the database URL, falling back to the default when not provided."""
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_engine(echo: bool | None = None):
    """Create a SQLAlchemy engine for the configured database."""
    echo = bool(os.getenv("SQLALCHEMY_ECHO", "0")) if echo is None else echo
    return create_engine(get_database_url(), echo=echo, future=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_session():
    """Provide a session generator suitable for FastAPI dependencies."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
