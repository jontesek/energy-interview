import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..api.schemas.devices import DeviceCreate, DeviceUpdate
from ..api.schemas.metrics import (
    MetricValueResponse,
    SubscriptionCreate,
    SubscriptionCreateResponse,
)
from .models import (
    Device,
    Metric,
    MetricValue,
    Site,
    SiteUser,
    Subscription,
    SubscriptionMetric,
    UserRole,
)


class Repository:
    def __init__(self, db: Session, user_id: int) -> None:
        self.db = db
        self.user_id = user_id

    # SITES
    def _has_user_access(self, site_id: int, required_role: str) -> bool:
        user_access = (
            self.db.query(SiteUser)
            .filter_by(site_id=site_id, user_id=self.user_id)
            .one_or_none()
        )
        # No access record
        if user_access is None:
            return False
        # Check permissions
        user_role = user_access.role
        # User has the same role as required
        if user_role == required_role:
            return True
        # User has lower role than required
        if user_role == UserRole.BASIC and required_role == UserRole.TECH:  # noqa: SIM103
            return False
        # User has higher role than required
        return True

    def get_site(self, site_id: int) -> Site | None:
        # Check access
        if not self._has_user_access(site_id, UserRole.BASIC):
            raise UnauthorizedError(site_id, self.user_id)
        # Get data
        return self.db.get(Site, site_id)

    def get_sites(self) -> list[Site] | None:
        all_sites = self.db.query(Site).all()
        allowed_sites = []
        # Check access for each site
        for site in all_sites:
            if self._has_user_access(site.id, UserRole.BASIC):
                allowed_sites.append(site.id)
        # Get data for allowed sites
        return self.db.query(Site).filter(Site.id.in_(allowed_sites)).all()

    # DEVICES
    def create_device(self, payload: DeviceCreate) -> int:
        if not self._has_user_access(payload.site_id, UserRole.TECH):
            raise UnauthorizedError(payload.site_id, self.user_id)
        device = Device(**payload.model_dump())
        device.created_by_user_id = self.user_id
        self.db.add(device)
        self.db.flush()
        return device.id

    def get_device(
        self, device_id: int, required_role: str = UserRole.BASIC
    ) -> Device | None:
        # Get site ID
        device = self.db.get(Device, device_id)
        if device is None:
            return None
        site_id = device.site_id
        # Check access
        if not self._has_user_access(site_id, required_role):
            raise UnauthorizedError(site_id, self.user_id)
        # Return data
        return device

    def get_site_devices(self, site_id: int) -> list[Device] | None:
        if not self._has_user_access(site_id, UserRole.BASIC):
            raise UnauthorizedError(site_id, self.user_id)
        return self.db.query(Device).filter_by(site_id=site_id).all()

    def update_device(self, device_id: int, payload: DeviceUpdate) -> Device | None:
        # Check access to device and get device site ID
        device = self.get_device(device_id, UserRole.TECH)
        if device is None:
            return None
        # If new site ID provided, check access
        update_data = payload.model_dump(exclude_unset=True)
        if new_site_id := update_data.get("site_id"):
            has_access = self._has_user_access(new_site_id, UserRole.TECH)
            if not has_access:
                raise UnauthorizedError(new_site_id, self.user_id)
        # All good - update data
        for key, value in update_data.items():
            setattr(device, key, value)
        return device

    def delete_device(self, device_id: int) -> Device | None:
        # check access done here
        device = self.get_device(device_id, UserRole.TECH)
        if device:
            self.db.delete(device)
        return device

    # METRICS
    def get_latest_metric_value(self, metric_id: int) -> MetricValueResponse | None:
        metric = self.db.get(Metric, metric_id)
        if metric is None:
            raise EntityNotFoundError("Metric", metric_id)

        latest_value = (
            self.db.query(MetricValue)
            .filter_by(metric_id=metric_id)
            .order_by(MetricValue.measured_at.desc())
            .first()
        )
        if latest_value is None:
            return None

        return MetricValueResponse(
            name=metric.name,
            unit=metric.unit,
            value=latest_value.value,
            measured_at=latest_value.measured_at,
        )

    def create_subscription(
        self, payload: SubscriptionCreate
    ) -> SubscriptionCreateResponse:
        # Check if all supplied metrics exist
        metric_ids = payload.metric_ids
        if not metric_ids:
            raise ValueError("metric_ids must not be empty")
        metrics = self.db.query(Metric).filter(Metric.id.in_(metric_ids)).all()
        if len(metric_ids) != len(metrics):
            raise EntityNotFoundError("Metric", None)
        # Create subscription
        subscription = Subscription(
            name=payload.name,
            description=payload.description,
            created_by_user_id=self.user_id,
        )
        self.db.add(subscription)
        self.db.flush()
        # Create subscription metrics
        for metric_id in metric_ids:
            met_subs = SubscriptionMetric(
                subscription_id=subscription.id, metric_id=metric_id
            )
            self.db.add(met_subs)
        # All good
        return SubscriptionCreateResponse(id=subscription.id)

    def get_metric_history(
        self, metric_id: int, start_dt: datetime.datetime, end_dt: datetime.datetime
    ) -> list[float]:
        metric = self.db.get(Metric, metric_id)
        if metric is None:
            raise EntityNotFoundError("Metric", metric_id)
        stmt = (
            select(MetricValue.value)
            .where(MetricValue.metric_id == metric_id)
            .where(MetricValue.measured_at.between(start_dt, end_dt))
        )
        values = self.db.execute(stmt).scalars().all()
        return list(values)


class UnauthorizedError(Exception):
    def __init__(self, site_id: int, user_id: int) -> None:
        super().__init__(f"User {user_id} cannot operate on site {site_id}.")


class EntityNotFoundError(Exception):
    def __init__(self, name: str, id: int | None) -> None:
        super().__init__(f"Entity {name} with ID {id} not found.")
