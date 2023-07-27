from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.exception.exception import EntityNotFoundException, EntityAlreadyExistsException, BadRequestException
from api.schemas.role_schemas import RoleOut, RoleCreate, RoleUpdate
from api.service.role_service import RoleService

router = APIRouter(tags=['Roles'])
role_service = RoleService()


@router.post('/api/roles', status_code=status.HTTP_201_CREATED, response_model=RoleOut)
def save_role(role_create: RoleCreate, db: Session = Depends(get_db)):
    try:
        return role_service.save(role_create, db)
    except EntityAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
    except BadRequestException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get('/api/roles/name', status_code=status.HTTP_200_OK, response_model=RoleOut)
def get_role_by_name(name: str, db: Session = Depends(get_db)):
    try:
        return role_service.get_role_by_name(name, db)
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/api/roles", status_code=status.HTTP_200_OK, response_model=List[RoleOut])
def get_all_roles(db: Session = Depends(get_db)):
    return role_service.get_all(db)


@router.put("/api/roles", status_code=status.HTTP_200_OK, response_model=RoleOut)
def update_role(role: RoleUpdate, db: Session = Depends(get_db)):
    try:
        return role_service.update_role(role, db)
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except EntityAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
