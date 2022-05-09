import json

DATA = {"title": "Новый пост",
        'text': 'Новый тест',
        "file_url": "media/img/2022-05-07_03-31-06.png",
        "file_type": "image/png",
        }


def test_create_user(client):
    """Тестируем создание пользователя."""
    data = DATA
    response = client.post("/posts/", json.dumps(data))
    assert response.status_code == 200


def test_all_posts(client):
    data = DATA
    client.post("/posts/", json.dumps(data))
    client.post("/posts/", json.dumps(data))
    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_update_post(client):
    data = DATA
    client.post("/posts/", json.dumps(data))
    data["title"] = "Еще новее"
    response = client.put("/posts/1", json.dumps(data))
    assert response.json()["post 1"] == 'updated'