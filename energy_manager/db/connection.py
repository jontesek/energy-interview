from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..settings import DB_CONN
from .models import Base


def get_db_session(db_conn: str, echo_sql: bool = False) -> Session:
    engine = create_engine(db_conn, echo=echo_sql)
    return Session(engine)


def create_db(db_conn: str, drop_first=False) -> Engine:
    engine = create_engine(db_conn)
    with engine.connect() as conn:
        if drop_first:
            Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn, checkfirst=True)
        conn.commit()
    return engine


def get_db(echo_sql: bool = False):
    db_url = DB_CONN
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
        if db_url.startswith("sqlite")
        else {},
        echo=echo_sql,
    )
    SessionLocal = sessionmaker(bind=engine)
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
