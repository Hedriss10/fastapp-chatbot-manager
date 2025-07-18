# test/unit/app/routes/test_users.py

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


URL_TEST = "http://127.0.0.1:8000"


def test_list_users_route(client):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


@patch("app.routes.users.UserCore.add_users")
def test_create_user_success(mock_add_users):
    mock_add_users.return_value = {
        "id": 1,
        "username": "john",
        "lastname": "doe",
        "phone": "11999999999",
    }

    payload = {"username": "john", "lastname": "doe", "phone": "11999999999"}

    response = client.post("/users", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "john",
        "lastname": "doe",
        "phone": "11999999999",
        "message_id": "user_created_successfully",
    }


@patch("app.routes.users.UserCore.update_users")
def test_update_user_success(mock_update_users):
    mock_update_users.return_value = {
        "message_id": "user_updated_successfully"
    }

    payload = {"username": "john", "lastname": "doe", "phone": "11999999999"}

    response = client.put("/users/1", json=payload)

    assert response.status_code == 200
    assert response.json() == {"message_id": "user_updated_successfully"}


@patch("app.routes.users.UserCore.add_users")
def test_create_user_invalid_payload(mock_add_users):
    mock_add_users.return_value = None
    payload = {"lastname": "sem_username", "phone": "999999999"}

    response = client.post("/users", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()
    assert "detail" in response.json()


@patch("app.routes.users.UserCore.delete_users")
def test_delete_users(mock_delete_users):
    mock_delete_users.return_value = {
        "message_id": "user_deleted_successfully"
    }
    response = client.delete("/users/1")
    assert response.status_code == 200
