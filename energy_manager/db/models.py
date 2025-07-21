import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Site(Base):
    __tablename__ = "site"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    name: Mapped[str]
    description: Mapped[str | None]
    created_at: Mapped[datetime.datetime]


class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("site.id"))
    name: Mapped[str]
    description: Mapped[str | None]
    created_at: Mapped[datetime.datetime]


class Metric(Base):
    __tablename__ = "metric"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))
    name: Mapped[str]
    unit: Mapped[str]
    description: Mapped[str | None]
    created_at: Mapped[datetime.datetime]


class MetricValue(Base):
    __tablename__ = "metric_value"

    metric_id: Mapped[int] = mapped_column(ForeignKey("metric.id"), primary_key=True)
    measured_at: Mapped[datetime.datetime] = mapped_column(primary_key=True)
    value: Mapped[float]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime.datetime]


class SiteUser(Base):
    __tablename__ = "site_user"

    site_id: Mapped[int] = mapped_column(ForeignKey("site.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    role: Mapped[str]
    assigned_at: Mapped[datetime.datetime]


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime.datetime]


class SubscriptionMetric(Base):
    __tablename__ = "subscription_metric"

    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscription.id"), primary_key=True
    )
    metric_id: Mapped[int] = mapped_column(ForeignKey("metric.id"), primary_key=True)
