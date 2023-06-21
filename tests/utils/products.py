import json
from fastapi.testclient import TestClient
from backend.crud.crud_catalog import CRUDCatalog
from backend.db.session import SessionLocal

from tests.utils.names import generate_random_name
session = SessionLocal()
product_data = {
    "name": "string",
    "price": 0,
    "characteristics": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    },
    "description": "string",

}
product_picture_ok = open(
    'tests/files/test_avatar.jpg', 'rb')


def create_product(client: TestClient, token_cookies, data, picture):
    response = client.post(
        "/products",
        headers=token_cookies,
        data={
            'product_data': json.dumps(data),
        },
        files={
            'ProductPicture': picture
        }
    )

    return response


def create_product_db(name=f"test_product_{generate_random_name(10)}", category_id=None):
    product = CRUDCatalog(session).create_category(
        name=name, category_id=category_id)
    return product
