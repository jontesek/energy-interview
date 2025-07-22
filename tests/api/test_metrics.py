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
