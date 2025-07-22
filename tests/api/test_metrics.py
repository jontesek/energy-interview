import pytest


@pytest.mark.parametrize(
    "metric_id, expected_value, status_code",
    [
        (1, 98, 200),
        (2, 2457, 200),
        (4, 6.1, 200),
        (6, None, 200),
        (99, None, 404),
    ],
)
def test_latest_metric_value(client, metric_id, expected_value, status_code):
    response = client.get(f"/metrics/{metric_id}/latest-value")
    assert response.status_code == status_code
    resp_json = response.json()
    value = None if resp_json is None else resp_json.get("value")
    assert value == expected_value


@pytest.mark.parametrize(
    "payload, status_code",
    [
        ({"name": "Wind turbine", "metric_ids": [4, 5, 6]}, 200),
        ({"name": "Wind turbine", "metric_ids": [4, 5, 666]}, 404),
        ({"name": "Wind turbine", "metric_ids": []}, 422),
    ],
)
def test_create_subscription(client, payload, status_code):
    headers = {"X-User-ID": "1"}
    response = client.post("/metrics/subscriptions", headers=headers, json=payload)
    assert response.status_code == status_code
