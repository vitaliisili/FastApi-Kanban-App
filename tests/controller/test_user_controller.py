import pytest
from api.schemas.user_schemas import UserOut


def test_get_all_user_success(authorized_admin_client, test_users):
    response = authorized_admin_client.get("/api/users")
    users = response.json()
    assert response.status_code == 200
    assert len(users) == len(test_users)


def test_get_all_user_unauthorized_user(client, test_users):
    response = client.get("/api/users")
    assert response.status_code == 401


def test_get_all_user_unauthorized_user_error_message(client, test_users):
    response = client.get("/api/users")
    error = response.json().get("detail")
    assert error == "Not authenticated"


def test_get_user_by_id_success(authorized_admin_client, test_simple_user):
    response = authorized_admin_client.get(f"/api/users/{test_simple_user.id}")
    user = UserOut(**response.json())
    assert response.status_code == 200
    assert user.email == test_simple_user.email


def test_get_user_by_id_unauthorized_user(client, test_simple_user):
    response = client.get(f"/api/users/{test_simple_user.id}")
    assert response.status_code == 401


def test_get_user_by_id_not_found_404(authorized_admin_client):
    response = authorized_admin_client.get("/api/users/21")
    assert response.status_code == 404


def test_get_user_by_id_error_message(authorized_admin_client):
    response = authorized_admin_client.get("/api/users/21")
    error = response.json().get("detail")
    assert error == "User with id: 21 not found"


@pytest.mark.parametrize("id", [
    "abc",
    32.12,
    "&21",
    "&id=1"
])
def test_get_user_by_id_not_valid_id(authorized_admin_client, id):
    response = authorized_admin_client.get(f"/api/users/{id}")
    assert response.status_code == 422


def test_get_user_by_id_not_valid_error_message(authorized_admin_client):
    response = authorized_admin_client.get(f"/api/users/not_valid_id")
    error = response.json().get("detail")
    assert error == "value is not a valid integer"


def test_update_user_success_update_email(authorized_admin_client, test_simple_user):
    data = {
        "id": test_simple_user.id,
        "email": "new_email@email.com",
        "first_name": test_simple_user.first_name,
        "last_name": test_simple_user.last_name,
        "roles": [
            {
                "id": test_simple_user.roles[0].id,
                "name": test_simple_user.roles[0].name
            }
        ]
    }
    response = authorized_admin_client.put("/api/users", json=data)
    user = UserOut(**response.json())
    assert response.status_code == 200
    assert user.email == test_simple_user.email


def test_update_user_unauthorized_user(client, test_simple_user):
    data = {
        "id": test_simple_user.id,
        "email": "new_email@email.com",
        "first_name": test_simple_user.first_name,
        "last_name": test_simple_user.last_name,
        "roles": [
            {
                "id": test_simple_user.roles[0].id,
                "name": test_simple_user.roles[0].name
            }
        ]
    }
    response = client.put("/api/users", json=data)
    assert response.status_code == 401


def test_update_user_success_update_first_name(authorized_admin_client, test_simple_user):
    data = {
        "id": test_simple_user.id,
        "email": test_simple_user.email,
        "first_name": "New First Name",
        "last_name": test_simple_user.last_name,
        "roles": [
            {
                "id": test_simple_user.roles[0].id,
                "name": test_simple_user.roles[0].name
            }
        ]
    }
    response = authorized_admin_client.put("/api/users", json=data)
    user = UserOut(**response.json())
    assert response.status_code == 200
    assert user.first_name == test_simple_user.first_name


def test_update_user_success_update_last_name(authorized_admin_client, test_simple_user):
    data = {
        "id": test_simple_user.id,
        "email": test_simple_user.email,
        "first_name": test_simple_user.first_name,
        "last_name": "New Last Name",
        "roles": [
            {
                "id": test_simple_user.roles[0].id,
                "name": test_simple_user.roles[0].name
            }
        ]
    }
    response = authorized_admin_client.put("/api/users", json=data)
    user = UserOut(**response.json())
    assert response.status_code == 200
    assert user.last_name == test_simple_user.last_name


def test_update_user_success_add_admin_role(authorized_admin_client, test_simple_user):
    data = {
        "id": test_simple_user.id,
        "email": test_simple_user.email,
        "first_name": test_simple_user.first_name,
        "last_name": test_simple_user.last_name,
        "roles": [
            {
                "id": 1,
                "name": "USER"
            },
            {
                "id": 2,
                "name": "ADMIN"
            }
        ]
    }

    response = authorized_admin_client.put("/api/users", json=data)
    user = UserOut(**response.json())
    assert response.status_code == 200
    assert len(user.roles) == len(test_simple_user.roles)
    assert user.roles[1].name == test_simple_user.roles[1].name


def test_update_user_not_found(authorized_admin_client):
    data = {
        "id": 99999,
        "email": "user@email.com",
        "first_name": "first_name",
        "last_name": "last_name",
        "roles": [
            {
                "id": 1,
                "name": "USER"
            },
        ]
    }
    response = authorized_admin_client.put("/api/users", json=data)
    assert response.status_code == 404


def test_update_user_not_found_error_message(authorized_admin_client):
    data = {
        "id": 99999,
        "email": "user@email.com",
        "first_name": "first_name",
        "last_name": "last_name",
        "roles": [
            {
                "id": 1,
                "name": "USER"
            },
        ]
    }
    response = authorized_admin_client.put("/api/users", json=data)
    error = response.json().get("detail")
    assert error == "User with id: 99999 not found"


def test_update_user_already_exist(authorized_admin_client, test_admin_user):
    data = {
        "id": 1,
        "email": test_admin_user.email,
        "first_name": "first_name",
        "last_name": "last_name",
        "roles": [
            {
                "id": 1,
                "name": "USER"
            },
        ]
    }

    response = authorized_admin_client.put("/api/users", json=data)
    assert response.status_code == 409


def test_update_user_already_exist_error_message(authorized_admin_client, test_admin_user):
    data = {
        "id": 1,
        "email": test_admin_user.email,
        "first_name": "first_name",
        "last_name": "last_name",
        "roles": [
            {
                "id": 1,
                "name": "USER"
            },
        ]
    }

    response = authorized_admin_client.put("/api/users", json=data)
    error = response.json().get("detail")
    assert error == f"User with email: {test_admin_user.email} already exists"


def test_delete_user_success(authorized_admin_client, test_simple_user):
    response = authorized_admin_client.delete(f"/api/users/{test_simple_user.id}")
    assert response.status_code == 204


def test_delete_user_unauthorized(client, test_simple_user):
    response = client.delete(f"/api/users/{test_simple_user.id}")
    assert response.status_code == 401


def test_delete_user_not_found(authorized_admin_client):
    response = authorized_admin_client.delete("/api/users/9999")
    assert response.status_code == 404


def test_delete_user_not_found_error_message(authorized_admin_client):
    response = authorized_admin_client.delete("/api/users/9999")
    error = response.json().get("detail")
    assert error == "User with id: 9999 not found"


@pytest.mark.parametrize("id", [
    "1a",
    "abc",
    "&id=1",
    1.1
])
def test_delete_user_not_found_wrong_id(authorized_admin_client, id):
    response = authorized_admin_client.delete(f"/api/users/{id}")
    error = response.json().get("detail")
    assert error == "value is not a valid integer"
