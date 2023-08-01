import pytest
from jose import jwt
from api.config.env_config import settings as env
from api.security.token_schemas import Token


def test_login_user_as_admin_success(client, test_admin_user, test_password):
    response = client.post("/api/auth/login", data={"username": test_admin_user.email, "password": test_password})
    assert response.status_code == 200


def test_login_user_as_user_success(client, test_simple_user, test_password):
    response = client.post("/api/auth/login", data={"username": test_simple_user.email, "password": test_password})
    assert response.status_code == 200


def test_login_as_admin_success_payload_token(client, test_admin_user, test_password):
    response = client.post("/api/auth/login", data={"username": test_admin_user.email, "password": test_password})
    token: Token = Token(**response.json())
    payload = jwt.decode(token.access_token, env.token_secret_key, algorithms=[env.token_algorithm])
    assert payload.get("email") == test_admin_user.email
    assert token.token_type == "Bearer"


def test_login_as_user_success_payload_token(client, test_simple_user, test_password):
    response = client.post("/api/auth/login", data={"username": test_simple_user.email, "password": test_password})
    token: Token = Token(**response.json())
    payload = jwt.decode(token.access_token, env.token_secret_key, algorithms=[env.token_algorithm])
    assert payload.get("email") == test_simple_user.email
    assert token.token_type == "Bearer"


def test_login_incorrect_email(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": "incorrect_email@email.com", "password": test_password})
    assert response.status_code == 403


def test_login_incorrect_email_error_message(client, test_users, test_password):
    response = client.post("/api/auth/login", data={"username": "incorrect_email@email.com", "password": test_password})
    error = response.json().get("detail")
    assert error == "Invalid Credentials"


def test_login_incorrect_password(client, test_admin_user, test_password):
    response = client.post("/api/auth/login", data={"username": test_admin_user, "password": "incorrect1A#"})
    assert response.status_code == 403


def test_login_incorrect_password_error_message(client, test_admin_user, test_password):
    response = client.post("/api/auth/login", data={"username": test_admin_user, "password": "incorrect1A#"})
    error = response.json().get("detail")
    assert error == "Invalid Credentials"


def test_save_user_success(client, test_roles, test_password):
    data = {"email": "new_user@email.com",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": test_password}

    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 201


def test_save_user_success_payload_token(client, test_roles, test_password):
    data = {"email": "new_user@email.com",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": test_password}

    response = client.post("/api/auth/register", json=data)
    token: Token = Token(**response.json())
    payload = jwt.decode(token.access_token, env.token_secret_key, algorithms=[env.token_algorithm])
    assert payload.get("email") == data.get("email")
    assert token.token_type == "Bearer"


def test_save_user_already_exist(client, test_simple_user, test_password):
    data = {"email": test_simple_user.email,
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": test_password}

    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 409


def test_save_user_already_exist_error_message(client, test_simple_user, test_password):
    data = {"email": test_simple_user.email,
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": test_password}

    response = client.post("/api/auth/register", json=data)
    error = response.json().get("detail")
    assert error == f"User with email: {data.get('email')} already exists"


@pytest.mark.parametrize("email, first_name, last_name, password", [
    ("", "Firstname", "Lastname", "password1A#"),
    ("test@email.com", "", "Lastname", "password1A#"),
    ("test@email.com", "Firstname", "", "password1A#"),
    ("test@email.com", "Firstname", "Lastname", ""),
])
def test_save_user_with_empty_data(client, test_users, email, first_name, last_name, password):
    data = {"email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password}

    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize("email", [
    "@mail.com", "#@%^%#$@#$@#.com", "email@example",
    "abc@.de", "email.example.com", "email@-example.com",
    "user@gmail.", ".email@example.com", "email@example..com",
    "user@user@gmail.com", "email.@example.com", "Abc..123@example.com"
])
def test_save_user_with_incorrect_email(client, test_users, email, test_password):
    data = {"email": email,
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": test_password}

    response = client.post("/api/auth/register", json=data)
    error = response.json().get("detail")
    assert response.status_code == 422
    assert error == "value is not a valid email address"


@pytest.mark.parametrize("password, error_message", [
    ("", "Password must be at least 8 characters long"),
    ("        ", "Password must contain at least 1 uppercase letter"),
    ("password", "Password must contain at least 1 uppercase letter"),
    ("passwordA", "Password must contain at least 1 digit"),
    ("passwordA1", "Password must contain at least 1 special character"),
])
def test_save_user_with_incorrect_password(client, test_users, password, error_message):
    data = {"email": "test@email.com",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "password": password}

    response = client.post("/api/auth/register", json=data)
    error = response.json().get("detail")
    assert response.status_code == 422
    assert error == error_message
