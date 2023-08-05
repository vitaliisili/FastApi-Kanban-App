from typing import List, Annotated, Type
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.exception.exception import EntityNotFoundException, EntityAlreadyExistsException, PermissionDeniedException
from api.models.user_model import User
from api.models.workspace_model import Workspace
from api.schemas.workspace_schemas import WorkspaceOut, WorkspaceCreate, WorkspaceUpdate
from api.security.jwt_config import get_principal
from api.service.workspace_service import WorkspaceService

router = APIRouter(tags=["Workspace"])
workspace_service = WorkspaceService()


@router.post("/api/workspaces", status_code=status.HTTP_201_CREATED, response_model=WorkspaceOut)
def save_workspace(workspace_create: WorkspaceCreate,
                   db: Session = Depends(get_db),
                   principal: User = Depends(get_principal)):
    try:
        new_workspace: Workspace = workspace_service.save_workspace(workspace_create, db, principal)
        return new_workspace
    except EntityAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/api/workspaces",
            status_code=status.HTTP_200_OK,
            response_model=List[WorkspaceOut],
            dependencies=[Depends(get_principal)])
def get_all_workspaces(db: Annotated[Session, Depends(get_db)]):
    workspaces = workspace_service.get_all_workspaces(db)
    return workspaces


@router.get("/api/workspaces/owner/{owner_id}",
            status_code=status.HTTP_200_OK,
            response_model=List[WorkspaceOut],
            dependencies=[Depends(get_principal)])
def get_all_workspaces_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    try:
        workspaces: List[Type[Workspace]] = workspace_service.get_all_workspaces_by_owner_id(owner_id, db)
        return workspaces
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/api/workspaces/{id}",
            status_code=status.HTTP_200_OK,
            response_model=WorkspaceOut,
            dependencies=[Depends(get_principal)])
def get_workspace_by_id(id: int, db: Session = Depends(get_db)):
    try:
        workspace: Type[Workspace] = workspace_service.get_workspace_by_id(id, db)
        return workspace
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.put("/api/workspaces", status_code=status.HTTP_200_OK, response_model=WorkspaceOut)
def update_workspace(workspace: WorkspaceUpdate,
                     db: Session = Depends(get_db),
                     principal: User = Depends(get_principal)):
    try:
        workspace: Type[Workspace] = workspace_service.update_workspace(workspace, db, principal)
        return workspace
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except PermissionDeniedException as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err))
