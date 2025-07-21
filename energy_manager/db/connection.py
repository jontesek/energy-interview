from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base


def get_db_session(db_conn: str, echo_sql: bool = False) -> Session:
    engine = create_engine(db_conn, echo=echo_sql)
    return Session(engine)


def create_db(db_conn: str, drop_first=False):
    engine = create_engine(db_conn)
    with engine.connect() as conn:
        if drop_first:
            Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn, checkfirst=True)
        conn.commit()
