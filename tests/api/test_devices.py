import pytest


@pytest.mark.parametrize(
    "device_id, user_id, status_code",
    [
        (1, 1, 200),
        (1, 3, 403),
        (3, 3, 200),
    ],
)
def test_get_device(client, device_id, user_id, status_code):
    headers = {"X-User-ID": str(user_id)}
    response = client.get(f"/devices/{device_id}", headers=headers)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "device_id, user_id, payload, status_code",
    [
        (1, 1, {"site_id": 2}, 403),
        (1, 1, {"name": "battery"}, 200),
        (1, 2, {"site_id": 2}, 200),
        (3, 3, {"name": "test"}, 403),
        (999, 1, {"site_id": 1}, 404),
    ],
)
def test_update_device(client, device_id, user_id, payload, status_code):
    headers = {"X-User-ID": str(user_id)}
    response = client.put(f"/devices/{device_id}", headers=headers, json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "device_id, user_id, status_code",
    [
        (4, 2, 200),
        (3, 1, 403),
        (3, 3, 403),
    ],
)
def test_delete_device(client, device_id, user_id, status_code):
    headers = {"X-User-ID": str(user_id)}
    response = client.delete(f"/devices/{device_id}", headers=headers)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "user_id, payload, status_code",
    [
        (2, {"site_id": 2, "name": "wind turbine"}, 200),
        (1, {"site_id": 2}, 422),
        (3, {"site_id": 2, "name": "test"}, 403),
    ],
)
def test_create_device(client, user_id, payload, status_code):
    headers = {"X-User-ID": str(user_id)}
    response = client.post("/devices", json=payload, headers=headers)
    assert response.status_code == status_code
