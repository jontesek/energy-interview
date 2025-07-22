# ruff: noqa: S106
import datetime

from ..settings import DB_CONN
from .connection import create_db, get_db_session
from .models import Device, Metric, MetricValue, Site, SiteUser, User


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
    # Metrics
    metrics = [
        Metric(device_id=1, name="charge level", unit="%"),
        Metric(device_id=2, name="pv power", unit="w"),
        Metric(device_id=3, name="charge level", unit="%"),
        Metric(device_id=4, name="wind speed", unit="m/s"),
        Metric(device_id=4, name="wind power", unit="w"),
        Metric(device_id=4, name="wind direction", unit="°"),
    ]
    db_session.add_all(metrics)
    # Metric values
    metric_values = [
        # Device 1
        MetricValue(
            metric_id=1, value=100, measured_at=datetime.datetime(2025, 6, 1, 1, 0, 0)
        ),
        MetricValue(
            metric_id=1, value=99, measured_at=datetime.datetime(2025, 6, 1, 1, 1, 0)
        ),
        MetricValue(
            metric_id=1, value=98, measured_at=datetime.datetime(2025, 6, 1, 1, 2, 0)
        ),
        # Device 2
        MetricValue(
            metric_id=2, value=2500, measured_at=datetime.datetime(2025, 6, 1, 10, 0, 0)
        ),
        MetricValue(
            metric_id=2, value=2531, measured_at=datetime.datetime(2025, 6, 1, 10, 1, 0)
        ),
        MetricValue(
            metric_id=2, value=2489, measured_at=datetime.datetime(2025, 6, 1, 10, 2, 0)
        ),
        MetricValue(
            metric_id=2, value=2457, measured_at=datetime.datetime(2025, 6, 1, 10, 3, 0)
        ),
        # Device 3
        MetricValue(
            metric_id=3, value=90, measured_at=datetime.datetime(2025, 6, 1, 1, 0, 0)
        ),
        MetricValue(
            metric_id=3, value=80, measured_at=datetime.datetime(2025, 6, 1, 2, 0, 0)
        ),
        MetricValue(
            metric_id=3, value=72, measured_at=datetime.datetime(2025, 6, 1, 3, 0, 0)
        ),
        MetricValue(
            metric_id=3, value=63, measured_at=datetime.datetime(2025, 6, 1, 4, 0, 0)
        ),
        MetricValue(
            metric_id=3, value=55, measured_at=datetime.datetime(2025, 6, 1, 5, 0, 0)
        ),
        # Device 4
        MetricValue(
            metric_id=4, value=5.3, measured_at=datetime.datetime(2025, 6, 1, 16, 0, 0)
        ),
        MetricValue(
            metric_id=4, value=5.7, measured_at=datetime.datetime(2025, 6, 1, 16, 1, 0)
        ),
        MetricValue(
            metric_id=4, value=6.1, measured_at=datetime.datetime(2025, 6, 1, 16, 2, 0)
        ),
        MetricValue(
            metric_id=5, value=1000, measured_at=datetime.datetime(2025, 6, 1, 16, 0, 0)
        ),
        MetricValue(
            metric_id=5, value=1100, measured_at=datetime.datetime(2025, 6, 1, 16, 1, 0)
        ),
        MetricValue(
            metric_id=5, value=1200, measured_at=datetime.datetime(2025, 6, 1, 16, 2, 0)
        ),
    ]
    db_session.add_all(metric_values)

    # Permanently save to DB
    db_session.commit()


if __name__ == "__main__":
    create_db(DB_CONN, drop_first=True)
    session = get_db_session(DB_CONN, echo_sql=True)
    insert_data(session)
    session.close()
