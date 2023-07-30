from jose import jwt
from api.config.env_config import settings as env
from api.security.token_schemas import Token


def test_login_user_as_admin_success(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": test_users[1].email, "password": test_password})
    assert response.status_code == 200


def test_login_user_as_user_success(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": test_users[0].email, "password": test_password})
    assert response.status_code == 200


def test_login_as_admin_success_payload_token(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": test_users[1].email, "password": test_password})
    token: Token = Token(**response.json())
    payload = jwt.decode(token.access_token, env.token_secret_key, algorithms=[env.token_algorithm])
    assert payload.get("email") == test_users[1].email
    assert token.token_type == "Bearer"


def test_login_as_user_success_payload_token(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": test_users[0].email, "password": test_password})
    token: Token = Token(**response.json())
    payload = jwt.decode(token.access_token, env.token_secret_key, algorithms=[env.token_algorithm])
    assert payload.get("email") == test_users[0].email
    assert token.token_type == "Bearer"


def test_login_incorrect_email(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": "incorrect_email@email.com", "password": test_password})
    assert response.status_code == 403


def test_login_incorrect_email_error_message(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": "incorrect_email@email.com", "password": test_password})
    error = response.json().get("detail")
    assert error == "Invalid Credentials"


def test_login_incorrect_password(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": test_users[1], "password": "incorrect1A#"})
    assert response.status_code == 403


def test_login_incorrect_password_error_message(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": test_users[1], "password": "incorrect1A#"})
    error = response.json().get("detail")
    assert error == "Invalid Credentials"
