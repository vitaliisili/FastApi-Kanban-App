import pytest
from api.schemas import user_schemas


@pytest.mark.parametrize("data", [
    ({"email": "simple@email.com",
      "password": "simplePassword1A#",
      "first_name": "SimpleFirst",
      "last_name": "SimpleLast"}),

    ({"email": "email_underscore@email.com",
      "password": "simplePassword1A#",
      "first_name": "lower",
      "last_name": "lowe"}),

    ({"email": "simple-dash@email.com",
      "password": "simplePassword1A#",
      "first_name": "First",
      "last_name": "Last"}),
])
def test_save_user_success(client, test_roles, data):
    response = client.post("/api/users", json=data)
    user = user_schemas.User(**response.json())
    assert response.status_code == 201
    assert user.roles[0].name == "USER"


def test_save_user_already_exist_error(client, test_users):
    data = {"email": "user@email.com",
            "password": "simplePassword1A#",
            "first_name": "SimpleFirst",
            "last_name": "SimpleLast"}

    response = client.post("/api/users", json=data)
    error = response.json().get("detail")
    assert response.status_code == 409
    assert error == f"User with email: {data['email']} already exists"


def test_get_all_user_success(client, test_users):
    response = client.get("/api/users")
    users = response.json()
    assert response.status_code == 200
    assert len(users) == len(test_users)
