import json

from back.models import helper


def test_valid_login(client, user_data):
    helper.add_user(user_data)

    payload = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200


def test_bad_login(client, user_data):
    helper.add_user(user_data)

    response = client.post("/api/auth/login", json={})
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data["message"] == "Empty json"

    missing_payload = {
        "password": user_data["password"]
    }
    response = client.post("/api/auth/login", json=missing_payload)
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data["message"] == "Badly formatted json"

    wrong_password = {
        "email": user_data["email"],
        "password": user_data["password"] + "f"
    }
    response = client.post("/api/auth/login", json=wrong_password)
    data = json.loads(response.data.decode())
    assert response.status_code == 403
    assert data["message"] == "Bad Credentials"
