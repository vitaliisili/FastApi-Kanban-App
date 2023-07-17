import pytest
from api.schemas import role_schemas


def test_save_role_success(client):
    role_test = {"name": "TEST"}
    response = client.post("/api/roles", json=role_test)
    new_role = role_schemas.Role(**response.json())
    assert response.status_code == 201
    assert new_role.name == role_test.get('name')


@pytest.mark.parametrize("name, status_code, error_message", [
    ("", 400, "Role name must not be blank"),
    (" ", 400, "Role name must not be blank"),
    ("   ", 400, "Role name must not be blank")
])
def test_save_role_empty_name_error(client, name, status_code, error_message):
    role_test = {"name": name}
    response = client.post("/api/roles", json=role_test)
    error = response.json().get("detail")
    assert response.status_code == status_code
    assert error == error_message


@pytest.mark.parametrize("name, status_code", [
    ("USER", 409),
    ("ADMIN", 409),
])
def test_save_role_with_existing_name_error(client, test_roles, name, status_code):
    existing_role = {"name": name}
    response = client.post("/api/roles", json=existing_role)
    error = response.json().get("detail")
    assert response.status_code == status_code
    assert error == f"Role with name {name} already exists"


def test_get_all_roles(client, test_roles):
    response = client.get("/api/roles")
    roles = list(map(lambda role: role_schemas.Role(**role), response.json()))
    assert response.status_code == 200
    assert len(roles) == len(test_roles)
