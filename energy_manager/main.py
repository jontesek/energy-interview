# ruff: noqa
from energy_manager.db.connection import create_db, get_db_session
from energy_manager.settings import DB_CONN


def main():
    # test db
    create_db(DB_CONN)
    session = get_db_session(DB_CONN, echo_sql=True)
    from energy_manager.db.models import User
    import datetime

    usr = User(
        name="Josef Novák",
        username="josef.novak",
        password="abcd",
        created_at=datetime.datetime.now(),
    )
    session.add(usr)
    session.commit()


if __name__ == "__main__":
    main()
