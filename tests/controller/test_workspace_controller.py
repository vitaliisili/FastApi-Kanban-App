from typing import List
import pytest
from api.schemas.workspace_schemas import WorkspaceOut


def test_save_workspace_success(authorized_admin_client):
    data = {"title": "New Test workspace"}
    response = authorized_admin_client.post("/api/workspaces", json=data)
    assert response.status_code == 201


def test_save_workspace_success_data(authorized_admin_client, test_users):
    data = {"title": "New Test workspace"}
    response = authorized_admin_client.post("/api/workspaces", json=data)
    workspace = WorkspaceOut(**response.json())
    assert workspace.title == data.get("title")
    assert workspace.owner_id == test_users[1].id
    assert workspace.members[0].email == test_users[1].email


def test_save_workspace_unidentified_user(client):
    data = {"title": "New Test workspace"}
    response = client.post("/api/workspaces", json=data)
    assert response.status_code == 401


def test_save_workspace_already_exists(authorized_admin_client, test_admin_workspaces):
    data = {"title": test_admin_workspaces[0].title}
    response = authorized_admin_client.post("/api/workspaces", json=data)
    assert response.status_code == 409


def test_save_workspace_already_exists_error_message(authorized_admin_client, test_admin_workspaces):
    data = {"title": test_admin_workspaces[0].title}
    response = authorized_admin_client.post("/api/workspaces", json=data)
    error = response.json().get("detail")
    assert error == f"Workspace with title: {data.get('title')} already exists"


@pytest.mark.parametrize("title", [
    "",
    " ",
    "     "
])
def test_save_workspace_empty_title(authorized_admin_client, title):
    data = {"title": title}
    response = authorized_admin_client.post("/api/workspaces", json=data)
    error = response.json().get("detail")
    assert response.status_code == 422
    assert error == "Title cannot be empty or blank"


def test_get_all_workspaces_success(authorized_admin_client, test_workspaces):
    response = authorized_admin_client.get("/api/workspaces")
    assert response.status_code == 200


def test_get_all_workspace_success_data(authorized_admin_client, test_workspaces):
    response = authorized_admin_client.get("/api/workspaces")
    workspaces = response.json()
    assert len(workspaces) == len(test_workspaces)
    assert workspaces[0].get("title") == test_workspaces[0].title


def test_get_all_unidentified_user(client, test_workspaces):
    response = client.get("/api/workspaces")
    assert response.status_code == 401


def test_get_all_unidentified_user_error_message(client, test_workspaces):
    response = client.get("/api/workspaces")
    error = response.json().get("detail")
    assert error == "Not authenticated"


def test_get_all_workspaces_by_owner_id_success(authorized_admin_client, test_workspaces, test_users):
    response = authorized_admin_client.get(f"/api/workspaces/{test_users[0].id}")
    assert response.status_code == 200


def test_get_all_workspaces_by_owner_id_success_data(authorized_admin_client,
                                                     test_workspaces,
                                                     test_users,
                                                     test_user_workspaces):
    response = authorized_admin_client.get(f"/api/workspaces/{test_users[0].id}")
    workspaces: List[WorkspaceOut] = response.json()
    assert len(workspaces) == len(test_user_workspaces)


def test_get_all_workspaces_by_owner_id_not_found(authorized_admin_client, test_workspaces):
    response = authorized_admin_client.get("/api/workspaces/9999")
    assert response.status_code == 404


def test_get_all_workspaces_by_owner_id_not_found_error_message(authorized_admin_client, test_workspaces):
    response = authorized_admin_client.get("/api/workspaces/9999")
    error = response.json().get("detail")
    assert error == f"User with id: 9999 not found"


def test_get_all_workspaces_by_owner_id_unauthorized_user(client, test_workspaces, test_users):
    response = client.get(f"/api/workspaces/{test_users[0].id}")
    assert response.status_code == 401


def test_get_all_workspaces_by_owner_id_unauthorized_user_error_message(client, test_workspaces, test_users):
    response = client.get(f"/api/workspaces/{test_users[0].id}")
    error = response.json().get("detail")
    assert error == "Not authenticated"
