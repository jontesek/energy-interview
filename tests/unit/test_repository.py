import pytest

from energy_manager.db.repositories import Repository, UserRole


@pytest.mark.parametrize(
    "site_id, user_id, required_role, has_access",
    [
        (1, 1, UserRole.BASIC, True),
        (1, 2, UserRole.TECH, True),
        (2, 2, UserRole.BASIC, True),
        (1, 3, UserRole.BASIC, False),
        (1, 3, UserRole.TECH, False),
        (3, 1, UserRole.BASIC, False),
    ],
)
def test_has_user_access(db_session, site_id, user_id, required_role, has_access):
    repo = Repository(db_session, user_id)
    assert repo._has_user_access(site_id, required_role) == has_access
