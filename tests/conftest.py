# ruff: noqa: E402
# Must set env var now
import os

DB_CONN = "sqlite:///energy_test.db"
os.environ["DB_CONN"] = DB_CONN

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from energy_manager.app import app as fast_api_app
from energy_manager.db.connection import create_db
from energy_manager.db.insert_sample_data import insert_data


@pytest.fixture(scope="module")
def db_session():
    db_engine = create_db(db_conn=DB_CONN, drop_first=True)
    db_session = Session(db_engine)
    insert_data(db_session)
    yield db_session
    db_session.close()


@pytest.fixture(scope="module")
def client(db_session):
    yield TestClient(fast_api_app)
