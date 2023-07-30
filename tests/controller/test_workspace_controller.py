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
