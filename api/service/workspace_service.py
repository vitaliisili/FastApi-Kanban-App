from typing import List, Type
from sqlalchemy.orm import Session
from api.exception.exception import EntityAlreadyExistsException, EntityNotFoundException, PermissionDeniedException
from api.models.user_model import User
from api.models.workspace_model import Workspace
from api.repository.workspace_repository import WorkspaceRepository
from api.schemas.workspace_schemas import WorkspaceCreate, WorkspaceUpdate
from api.service.user_service import UserService


class WorkspaceService:
    def __init__(self):
        self.workspace_repository = WorkspaceRepository(Workspace)
        self.user_service = UserService()

    def save_workspace(self, workspace_create: WorkspaceCreate, db: Session, principal: User) -> Workspace:
        workspaces: List[Type[Workspace]] = self.workspace_repository.get_all_by_owner_id(principal.id, db)
        if workspace_create.title in [workspace.title for workspace in workspaces]:
            raise EntityAlreadyExistsException(f"Workspace with title: {workspace_create.title} already exists")

        new_workspace: Workspace = Workspace(**workspace_create.dict())
        new_workspace.owner_id = principal.id
        default_member = self.user_service.get_user_by_id(principal.id, db)
        new_workspace.members.append(default_member)
        return self.workspace_repository.save(new_workspace, db)

    def get_all_workspaces(self, db: Session) -> list[Type[Workspace]]:
        workspaces: List[Type[Workspace]] = self.workspace_repository.get_all(db)
        return workspaces

    def get_all_workspaces_by_owner_id(self, owner_id, db: Session) -> List[Type[Workspace]]:
        owner_check: Type[User] = self.user_service.get_user_by_id(owner_id, db)
        if not owner_check:
            raise EntityNotFoundException(f"User with owner_id: {owner_id} not found")
        workspaces: List[Type[Workspace]] = self.workspace_repository.get_all_by_owner_id(owner_id, db)
        return workspaces

    def get_workspace_by_id(self, id: int, db: Session) -> Type[Workspace]:
        workspace: Type[Workspace] = self.workspace_repository.get_by_id(id, db)
        if not workspace:
            raise EntityNotFoundException(f"Workspace with id: {id} not found")
        return workspace

    def update_workspace(self, workspace: WorkspaceUpdate, db: Session, principal: User):
        check_workspace: Workspace = self.workspace_repository.get_by_id(workspace.id, db)

        if check_workspace is None:
            raise EntityNotFoundException(f"Workspace with id: {workspace.id} not found")

        if check_workspace.owner_id != principal.id and "ADMIN" not in [role.name for role in principal.roles]:
            raise PermissionDeniedException("Access denied: not enough privileges")

        updated_workspace = self.workspace_repository.update(workspace, db)
        return updated_workspace

