import pytest
from api.schemas.role_schemas import RoleOut


def test_save_role_success(client):
    role = {"name": "TEST"}
    response = client.post("/api/roles", json=role)
    new_role = RoleOut(**response.json())
    assert response.status_code == 201
    assert new_role.name == role.get('name')


@pytest.mark.parametrize("name, status_code, error_message", [
    ("", 400, "Role name must not be blank"),
    (" ", 400, "Role name must not be blank"),
    ("   ", 400, "Role name must not be blank")
])
def test_save_role_empty_name_error(client, name, status_code, error_message):
    role = {"name": name}
    response = client.post("/api/roles", json=role)
    error = response.json().get("detail")
    assert response.status_code == status_code
    assert error == error_message


@pytest.mark.parametrize("name, status_code", [
    ("USER", 409),
    ("ADMIN", 409),
    ("MODERATOR", 409),
])
def test_save_role_with_existing_name_error(client, test_roles, name, status_code):
    existing_role = {"name": name}
    response = client.post("/api/roles", json=existing_role)
    error = response.json().get("detail")
    assert response.status_code == status_code
    assert error == f"Role with name {name} already exists"


def test_get_all_roles(client, test_roles):
    response = client.get("/api/roles")
    roles = [RoleOut(**role) for role in response.json()]
    assert response.status_code == 200
    assert len(roles) == len(test_roles)


def test_update_role_success(client, test_roles):
    role = {
        "id": test_roles[2].id,
        "name": "MANAGER"
    }
    response = client.put("/api/roles", json=role)
    updated_role = RoleOut(**response.json())
    assert response.status_code == 200
    assert updated_role.name == test_roles[2].name


def test_update_role_not_found(client):
    role = {
        "id": 9999,
        "name": "MANAGER"
    }
    response = client.put("/api/roles", json=role)
    assert response.status_code == 404


def test_update_role_not_found_error_message(client):
    role = {
        "id": 9999,
        "name": "MANAGER"
    }
    response = client.put("/api/roles", json=role)
    error = response.json().get("detail")
    assert error == "Role with id: 9999 not found"


@pytest.mark.parametrize("name", [
    "USER",
    "ADMIN"
])
def test_update_role_already_exist(client, test_roles, name):
    role = {
        "id": test_roles[2].id,
        "name": name
    }
    response = client.put("/api/roles", json=role)
    assert response.status_code == 409


@pytest.mark.parametrize("name", [
    "USER",
    "ADMIN"
])
def test_update_role_already_exist_error_message(client, test_roles, name):
    role = {
        "id": test_roles[2].id,
        "name": name
    }
    response = client.put("/api/roles", json=role)
    error = response.json().get("detail")
    assert error == f"Role with name: {name} already exists"


def test_delete_role_success(client, test_roles):
    response = client.delete(f"/api/roles/{test_roles[2].id}")
    assert response.status_code == 204


def test_delete_role_not_found(client):
    response = client.delete("/api/roles/9999")
    assert response.status_code == 404


def test_delete_role_not_found_error_message(client):
    response = client.delete("/api/roles/9999")
    error = response.json().get("detail")
    assert error == "Role with id: 9999 not found"


@pytest.mark.parametrize("id", [
    "abc",
    "%id=1",
    "&1",
    "&id=1",
    1.1
])
def test_delete_role_wrong_id(client, id):
    response = client.delete(f"/api/roles/{id}")
    assert response.status_code == 422


@pytest.mark.parametrize("id", [
    "abc",
    "%id=1",
    "&1",
    "&id=1",
    1.1
])
def test_delete_role_wrong_id_error_message(client, id):
    response = client.delete(f"/api/roles/{id}")
    error = response.json().get("detail")
    assert error == "value is not a valid integer"
