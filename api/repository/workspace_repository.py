from typing import List, Type
from sqlalchemy.orm import Session
from api.models.user_model import User
from api.models.workspace_model import Workspace
from api.repository.read_write_repository import ReadWriteRepository
from api.schemas.workspace_schemas import WorkspaceUpdate


class WorkspaceRepository(ReadWriteRepository):

    def get_all_by_owner_id(self, owner_id: int, db: Session) -> List[Type[Workspace]]:  # noqa
        workspaces: List[Type[Workspace]] = db.query(Workspace).filter_by(owner_id=owner_id).all()
        return workspaces

    def get_workspace_by_title(self, owner_id, workspace_title: str, db: Session) -> Workspace:  # noqa
        workspace: Workspace = db.query(Workspace).filter_by(owner_id=owner_id, title=workspace_title).firts()
        return workspace

    def update(self, workspace_update: WorkspaceUpdate, db: Session) -> Type[Workspace]:
        workspace: Type[Workspace] = db.query(Workspace).filter_by(id=workspace_update.id).first()

        for field, value in workspace_update.dict(exclude={"members"}).items():
            if value is not None:
                setattr(workspace, field, value)

        members_ids: List[int] = [user.id for user in workspace_update.members]
        members: List[Type[User]] = db.query(User).filter(User.id.in_(members_ids)).all()

        workspace.members = members

        db.commit()
        db.refresh(workspace)
        return workspace
