from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from railnav_backend import api, database, models


@pytest.fixture()
def db_session(tmp_path) -> Generator[Session, None, None]:
    db_url = f"sqlite:///{tmp_path/'test.db'}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False}, future=True)
    models.Base.metadata.create_all(bind=engine)

    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    original_engine = database.engine
    original_url = database.DATABASE_URL

    database.DATABASE_URL = db_url
    database.engine = engine

    try:
        session = session_factory()
        yield session
        session.commit()
    finally:
        session.close()
        database.engine = original_engine
        database.DATABASE_URL = original_url


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = api.create_app()

    def override_get_session() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[database.get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
