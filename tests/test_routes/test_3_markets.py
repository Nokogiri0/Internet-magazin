from fastapi.testclient import TestClient
data = {
    "address": "test_address",
    "phone": "+380501234567",
    "description": "test_description",
    "weekday_hours": "test_weekday_hours",
    "weekend_hours": "test_weekend_hours"
}


def create_market(client: TestClient, token_cookies, data: dict):
    response = client.post(
        "/markets",
        headers=token_cookies,
        json=data
    )
    return response


def test_create_markets(client: TestClient, normal_admin_token_cookies):
    for i in range(10):
        data["address"] = f"test_address_{i}"
        response = create_market(client, normal_admin_token_cookies, data)
        assert response.status_code == 201


def test_get_markets(client: TestClient, normal_user_token_cookies):
    response = client.get(
        "/markets",
        headers=normal_user_token_cookies,
    )
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_market(client: TestClient, normal_user_token_cookies):
    response = client.get(
        "/markets/1",
        headers=normal_user_token_cookies,
    )
    assert response.status_code == 200
    assert response.json()["address"] == "test_address_0"


def test_update_market(client: TestClient, normal_admin_token_cookies):
    data["address"] = "new_test_address"
    response = client.put(
        "/markets/1",
        headers=normal_admin_token_cookies,
        json=data
    )

    assert response.status_code == 200
    assert response.json()["address"] == "new_test_address"

    response = client.get(
        "/markets/1"
    )
    assert response.status_code == 200
    assert response.json()["address"] == "new_test_address"


def test_delete_market(client: TestClient, normal_admin_token_cookies):
    response = client.delete(
        "/markets/1",
        headers=normal_admin_token_cookies,
    )
    assert response.status_code == 204

    response = client.get(
        "/markets/1",
        headers=normal_admin_token_cookies,
    )
    assert response.status_code == 404


def test_delete_market_not_found(client: TestClient, normal_admin_token_cookies):
    response = client.delete(
        "/markets/100",
        headers=normal_admin_token_cookies,
    )
    assert response.status_code == 404


def test_update_market_not_found(client: TestClient, normal_admin_token_cookies):
    response = client.put(
        "/markets/100",
        headers=normal_admin_token_cookies,
        json=data
    )
    assert response.status_code == 404


def test_get_market_not_found(client: TestClient, normal_user_token_cookies):
    response = client.get(
        "/markets/100",
        headers=normal_user_token_cookies,
    )
    assert response.status_code == 404


def test_create_market_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.post(
        "/markets",
        headers=normal_user_token_cookies,
        json=data
    )
    assert response.status_code == 401


def test_update_market_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.put(
        "/markets/1",
        headers=normal_user_token_cookies,
        json=data
    )
    assert response.status_code == 401


def test_delete_market_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.delete(
        "/markets/1",
        headers=normal_user_token_cookies,
    )
    assert response.status_code == 401


def test_create_market_invalid_data(client: TestClient, normal_admin_token_cookies):
    data["address"] = ""
    response = client.post(
        "/markets",
        headers=normal_admin_token_cookies,
        json=data
    )
    assert response.status_code == 422


def test_update_market_invalid_data(client: TestClient, normal_admin_token_cookies):
    data["address"] = ""
    response = client.put(
        "/markets/3",
        headers=normal_admin_token_cookies,
        json=data
    )
    assert response.status_code == 422


def test_get_markets_not_authorized(client: TestClient):
    response = client.get(
        "/markets",
    )
    assert response.status_code == 200


def test_get_market_not_authorized(client: TestClient):
    response = client.get(
        "/markets/2",
    )
    assert response.status_code == 200
