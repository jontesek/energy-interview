from sqlalchemy.orm import Session

from .models import Site, SiteUser, UserRole


class Repository:
    def __init__(self, db: Session, user_id: int) -> None:
        self.db = db
        self.user_id = user_id

    # Site
    def _has_user_access(self, site_id: int, user_id: int, required_role: str) -> bool:
        user_access = (
            self.db.query(SiteUser)
            .filter_by(site_id=site_id, user_id=user_id)
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
        if not self._has_user_access(site_id, self.user_id, UserRole.BASIC):
            raise UnauthorizedError(site_id, self.user_id)
        # Get data
        return self.db.get(Site, site_id)

    def get_sites(self) -> list[Site] | None:
        all_sites = self.db.query(Site).all()
        allowed_sites = []
        # Check access for each site
        for site in all_sites:
            if self._has_user_access(site.id, self.user_id, UserRole.BASIC):
                allowed_sites.append(site.id)
        # Get data for allowed sites
        return self.db.query(Site).filter(Site.id.in_(allowed_sites)).all()


class UnauthorizedError(Exception):
    def __init__(self, site_id: int, user_id: int) -> None:
        super().__init__(f"User {user_id} cannot operate on site {site_id}.")
