"""Database configuration and session management for RailNav backend."""
from __future__ import annotations

from contextlib import contextmanager
from os import getenv
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "railnav.db"
DATABASE_URL = getenv("RAILNAV_DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")


def _build_engine(url: str = DATABASE_URL, echo: bool = False):
    """Construct a SQLAlchemy engine."""
    return create_engine(
        url,
        connect_args={"check_same_thread": False},
        echo=echo,
        future=True,
    )


engine = _build_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@contextmanager
def session_scope(echo: bool = False) -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    engine_to_use = engine if not echo else _build_engine(DATABASE_URL, echo=True)
    session_factory = sessionmaker(
        bind=engine_to_use, autoflush=False, autocommit=False, future=True
    )
    session: Session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    with session_scope() as session:
        yield session
