# test/unit/app/routes/test_users.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_users_route(client):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
