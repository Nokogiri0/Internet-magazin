import pytest
from fastapi.testclient import TestClient
from tests.utils.names import generate_random_name
from backend.crud.crud_catalog import CRUDCatalog
from backend.db.session import SessionLocal
from tests.utils.products import create_product_db, create_product, product_data, product_picture_ok

session = SessionLocal()
data = {
    "parent_id": None,
    "name": f"test_category_{generate_random_name(10)}",
    "parent_products_to_child": True,
}


def create_category_db(name=f"test_category_{generate_random_name(10)}", parent_id=None):
    category = CRUDCatalog(session).create_category(
        name=name, parent_id=parent_id)
    return category


def create_category(client: TestClient, token_cookies, data: dict):
    data["name"] = f"test_category_{generate_random_name(10)}"
    response = client.post(
        "/categories",
        headers=token_cookies,
        json=data
    )

    return response


def create_category_with_products_db():
    category = create_category_db()
    for i in range(10):
        create_product_db(category_id=category.id)
    return category


def create_category_with_products(client: TestClient, token_cookies, expected_status_code=201, data: dict = data):
    category = create_category(client, token_cookies, data)
    assert category.status_code == expected_status_code
    category_json = category.json()
    for i in range(10):
        product_data["category_id"] = category_json["id"]
        product = create_product(
            client, token_cookies, data=product_data, picture=product_picture_ok)
        assert product.status_code == expected_status_code
    return category


@pytest.mark.parametrize("parent_id", [None, 1, 2, 3])
def test_create_category(client: TestClient, normal_admin_token_cookies, parent_id):
    data["parent_id"] = parent_id
    response = create_category(client, normal_admin_token_cookies, data)
    assert response.status_code == 201


def test_get_categories(client: TestClient, normal_user_token_cookies):
    response = client.get(
        "/categories",
        headers=normal_user_token_cookies,
    )
    assert response.status_code == 200


def test_get_category(client: TestClient, normal_user_token_cookies):
    response = client.get(
        "/categories/1",
        headers=normal_user_token_cookies,
    )
    assert response.status_code == 200


def test_update_category(client: TestClient, normal_admin_token_cookies):
    category = create_category(client, normal_admin_token_cookies, data)
    category_json = category.json()
    assert category.status_code == 201
    new_name = f"test_category_{generate_random_name(10)}"
    data["name"] = new_name
    response = client.put(
        f"/categories/{category_json['id']}",
        headers=normal_admin_token_cookies,
        json=data
    )
    assert response.status_code == 200
    assert response.json()["name"] == new_name


def test_update_category_as_user(client: TestClient, normal_user_token_cookies, normal_admin_token_cookies):
    category = create_category(client, normal_admin_token_cookies, data)
    category_json = category.json()
    assert category.status_code == 201
    response = client.put(
        f"/categories/{category_json['id']}",
        headers=normal_user_token_cookies,
        json=data
    )
    assert response.status_code == 403


def test_create_subcategory_with_products_in_parent(client: TestClient, normal_admin_token_cookies):
    category = create_category_with_products(
        client, normal_admin_token_cookies)
    category_json = category.json()
    assert category.status_code == 201
    data["parent_id"] = category_json["id"]
    response = create_category(
        client, normal_admin_token_cookies, data)
    assert response.status_code == 400

    data["parent_products_to_child"] = True
    response = create_category(
        client, normal_admin_token_cookies, data)
    assert response.status_code == 201
