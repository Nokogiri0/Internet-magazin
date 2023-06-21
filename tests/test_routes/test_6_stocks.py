from fastapi.testclient import TestClient
from backend.crud.crud_products import CRUDProduct
from backend.crud.crud_catalog import CRUDCatalog
data = {
    "name": "stock_name",
    "open_date": "2023-01-30T15:51:16.734Z",
    "close_date": "2023-01-30T15:51:16.734Z",
    "description": "string",
    "products": [
    ]
}


def test_create_stock(client: TestClient, normal_user_token_headers, db_session):
    crud_product = CRUDProduct(db_session)
    crud_catalog = CRUDCatalog(db_session)
    catalog = crud_catalog.create_category(name="test_catalog", parent_id=None)
    data['products'] = [
        crud_product.create_product(
            name="test_product",
            description="test_description",
            price=10,
            category_id=catalog.get("id"),
            stock_id=None
        )
        for i in range(10)
    ]
    response = client.post(
        "/stocks", headers=normal_user_token_headers, json=data)
    assert response.status_code == 200
