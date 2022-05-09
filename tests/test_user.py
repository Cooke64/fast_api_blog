import json


def test_create_user(client):
    """Тестируем создание пользователя."""
    data = {"username": "testuser", "email": "123@mail.com",
            "password": "testing"}
    response = client.post("/user/", json.dumps(data))
    assert response.status_code == 201
    assert response.json()["email"] == "123@mail.com"
    assert response.json()["is_active"] is True
