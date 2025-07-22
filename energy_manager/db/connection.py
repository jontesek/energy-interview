from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..settings import DB_CONN, ECHO_SQL
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


# Generator for FastAPI dependency
def get_db():
    # Create engine
    db_url = DB_CONN
    echo_sql = bool(ECHO_SQL)
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
        if db_url.startswith("sqlite")
        else {},
        echo=echo_sql,
    )
    # Create session and close it after use
    SessionLocal = sessionmaker(bind=engine)
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
