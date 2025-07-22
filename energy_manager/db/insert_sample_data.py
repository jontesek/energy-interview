# ruff: noqa: S106
from ..settings import DB_CONN
from .connection import create_db, get_db_session
from .models import Device, Site, SiteUser, User


def insert_data(db_session):
    # Sites
    sites = [
        Site(
            address="Černokostelecká 2198/53, Praha, 100 00", name="Uzeniny Strašnice"
        ),
        Site(address="Vodní 254/9, Brno, 602 00", name="Vodárny Brno"),
        Site(address="Opavská 962/40, Ostrava, 708 00", name="Důl Poruba"),
    ]
    db_session.add_all(sites)
    # Users
    users = [
        User(name="Josef Novák", username="josef.novak", password="abcd"),
        User(name="Pavel Benda", username="pavel.benda", password="abcd"),
        User(name="Tomáš Sokol", username="tomas.sokol", password="abcd"),
        User(name="Alena Zámecká", username="alena.zamecka", password="abcd"),
    ]
    db_session.add_all(users)
    # SiteUsers
    site_users = [
        SiteUser(site_id=1, user_id=1, role="tech"),
        SiteUser(site_id=1, user_id=2, role="tech"),
        SiteUser(site_id=2, user_id=2, role="tech"),
        SiteUser(site_id=2, user_id=3, role="basic"),
        SiteUser(site_id=3, user_id=4, role="basic"),
    ]
    db_session.add_all(site_users)
    # Make objects available
    db_session.flush()
    # Devices
    devices = [
        Device(site_id=1, name="battery", created_by_user_id=1),
        Device(site_id=1, name="pv panel", created_by_user_id=1),
        Device(site_id=2, name="battery", created_by_user_id=1),
        Device(site_id=2, name="wind turbine", created_by_user_id=1),
    ]
    db_session.add_all(devices)

    # Permanently save to DB
    db_session.commit()


if __name__ == "__main__":
    create_db(DB_CONN, drop_first=True)
    session = get_db_session(DB_CONN, echo_sql=True)
    insert_data(session)
    session.close()
