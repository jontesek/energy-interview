import pytest
from fastapi import status


class TestDeviceCreate:
    def __run_test_case(self, client, user_id, payload, status_code):
        headers = {"X-User-ID": str(user_id)}
        response = client.post("/devices", json=payload, headers=headers)
        assert response.status_code == status_code

    def test_success(self, client):
        user_id = 2
        payload = {"site_id": 2, "name": "wind turbine"}
        status_code = status.HTTP_200_OK
        self.__run_test_case(client, user_id, payload, status_code)

    def test_missing_name(self, client):
        user_id = 1
        payload = {"site_id": 2}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.__run_test_case(client, user_id, payload, status_code)

    def test_forbidden(self, client):
        user_id = 3
        payload = {"site_id": 2, "name": "test"}
        status_code = status.HTTP_403_FORBIDDEN
        self.__run_test_case(client, user_id, payload, status_code)


class TestDeviceGet:
    def __run_test_case(self, client, device_id, user_id, status_code):
        headers = {"X-User-ID": str(user_id)}
        response = client.get(f"/devices/{device_id}", headers=headers)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "device_id, user_id",
        [(1, 1), (3, 3)],
    )
    def test_success(self, client, device_id, user_id):
        self.__run_test_case(client, device_id, user_id, status.HTTP_200_OK)

    def test_forbidden(self, client):
        device_id = 1
        user_id = 3
        status_code = status.HTTP_403_FORBIDDEN
        self.__run_test_case(client, device_id, user_id, status_code)


class TestDeviceUpdate:
    def __run_test_case(self, client, device_id, user_id, payload, status_code):
        headers = {"X-User-ID": str(user_id)}
        response = client.put(f"/devices/{device_id}", headers=headers, json=payload)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "device_id, user_id, payload",
        [
            (1, 1, {"name": "battery"}),
            (1, 2, {"site_id": 2}),
        ],
    )
    def test_success(self, client, device_id, user_id, payload):
        status_code = status.HTTP_200_OK
        self.__run_test_case(client, device_id, user_id, payload, status_code)

    @pytest.mark.parametrize(
        "device_id, user_id, payload",
        [
            (1, 1, {"site_id": 2}),
            (3, 3, {"name": "test"}),
        ],
    )
    def test_forbidden(self, client, device_id, user_id, payload):
        status_code = status.HTTP_403_FORBIDDEN
        self.__run_test_case(client, device_id, user_id, payload, status_code)

    def test_not_found(self, client):
        device_id = 999
        user_id = 1
        payload = {"site_id": 1}
        status_code = status.HTTP_404_NOT_FOUND
        self.__run_test_case(client, device_id, user_id, payload, status_code)


class TestDeviceDelete:
    def __run_test_case(self, client, device_id, user_id, status_code):
        headers = {"X-User-ID": str(user_id)}
        response = client.delete(f"/devices/{device_id}", headers=headers)
        assert response.status_code == status_code

    def test_success(self, client):
        device_id = 4
        user_id = 2
        status_code = status.HTTP_200_OK
        self.__run_test_case(client, device_id, user_id, status_code)

    @pytest.mark.parametrize(
        "device_id, user_id",
        [(3, 1), (3, 3)],
    )
    def test_forbidden(self, client, device_id, user_id):
        status_code = status.HTTP_403_FORBIDDEN
        self.__run_test_case(client, device_id, user_id, status_code)
