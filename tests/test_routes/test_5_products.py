from fastapi.testclient import TestClient
from backend.crud.crud_catalog import CRUDCatalog
from backend.db.session import SessionLocal
from tests.test_routes.test_4_categories import create_category_db
from tests.utils.names import generate_random_name
