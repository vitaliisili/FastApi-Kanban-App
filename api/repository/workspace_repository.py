from typing import List
from sqlalchemy.orm import Session
from api.models.workspace_model import Workspace
from api.repository.read_write_repository import ReadWriteRepository


class WorkspaceRepository(ReadWriteRepository):

    def get_all_by_owner_id(self, owner_id: int, db: Session) -> List[Workspace]:
        workspaces: List[Workspace] = db.query(Workspace).filter_by(owner_id=owner_id).all()
        return workspaces

    def get_workspace_by_title(self, owner_id, workspace_title: str, db: Session) -> Workspace:
        workspace: Workspace = db.query(Workspace).filter_by(owner_id=owner_id, title=workspace_title).firts()
        return workspace
