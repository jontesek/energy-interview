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


@pytest.mark.parametrize(
    "metric_id, start_dt, end_dt, metric_count, status_code",
    [
        (2, "2025-06-01 10:00:00", "2025-06-01 10:03:00", 4, 200),
        (3, "2025-06-01 02:00:00", "2025-06-01 04:00:00", 3, 200),
        (4, "2020-06-01 10:00:00", "2025-06-30 20:59:00", 3, 200),
        (1, "2025-06-01x10:00:00", "2025-06-01 10:03:00", None, 422),
        (1, "2024-06-01 10:00:00", "2024-06-01 10:03:00", 0, 200),
        (999, "2024-06-01 10:00:00", "2024-06-01 10:03:00", None, 404),
    ],
)
def test_metric_history(client, metric_id, start_dt, end_dt, metric_count, status_code):
    headers = {"X-User-ID": "1"}
    params = {"start_dt": start_dt, "end_dt": end_dt}
    response = client.get(
        f"/metrics/{metric_id}/history", headers=headers, params=params
    )
    assert response.status_code == status_code
    # Request OK, check number of returned values.
    if response.status_code == 200:
        assert len(response.json()) == metric_count
