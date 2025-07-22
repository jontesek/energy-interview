from sqlalchemy.orm import Session

from ..api.schemas.devices import DeviceCreate, DeviceUpdate
from .models import Device, Site, SiteUser, UserRole


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


class UnauthorizedError(Exception):
    def __init__(self, site_id: int, user_id: int) -> None:
        super().__init__(f"User {user_id} cannot operate on site {site_id}.")
