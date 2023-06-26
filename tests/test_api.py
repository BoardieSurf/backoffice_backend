from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_guest_permissions():
    response = client.get("http://localhost:8000/backoffice/info/image")

    assert response.status_code == 403
