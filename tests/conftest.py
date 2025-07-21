import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from energy_manager.app import create_app
from energy_manager.db.connection import create_db
from energy_manager.db.insert_sample_data import insert_data

DB_CONN = "sqlite:///energy_test.db"


@pytest.fixture(scope="session")
def db_session():
    db_engine = create_db(db_conn=DB_CONN, drop_first=True)
    db_session = Session(db_engine)
    insert_data(db_session)
    yield db_session
    db_session.close()


@pytest.fixture(scope="session")
def client(db_session):
    app = create_app(db_session=db_session, is_debug=False)
    yield TestClient(app)
