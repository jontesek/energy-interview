import pytest


@pytest.mark.parametrize(
    "user_id, site_count",
    [
        (1, 1),
        (2, 2),
        (3, 1),
    ],
)
def test_get_sites(client, user_id, site_count):
    headers = {"X-User-ID": str(user_id)}
    response = client.get("/sites", headers=headers)
    assert len(response.json()) == site_count


@pytest.mark.parametrize(
    "site_id, user_id, status_code",
    [
        (1, 1, 200),
        (1, 2, 200),
        (2, 2, 200),
        (1, 3, 403),
        (3, 1, 403),
    ],
)
def test_get_site(client, site_id, user_id, status_code):
    headers = {"X-User-ID": str(user_id)}
    response = client.get(f"/sites/{site_id}", headers=headers)
    assert response.status_code == status_code
