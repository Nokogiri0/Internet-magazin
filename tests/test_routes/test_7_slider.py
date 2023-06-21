import json
from fastapi.testclient import TestClient


def test_create_slide(client: TestClient, normal_admin_token_cookies):
    data = {
        "name": "slide_name",
        "open_date": "2023-01-30T15:51:16.734Z",
        "close_date": None,
        "url": "string",
        "position": 0,
        "is_active": True
    }
    response = client.post(
        "/slider",
        headers=normal_admin_token_cookies,
        json={"slide": data},
        files={
            "SlidePicture": open("tests/test_routes/test_7_slider.py", "rb")
        }
    )
    assert response.status_code == 201, response.json()
