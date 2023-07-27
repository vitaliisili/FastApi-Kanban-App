from typing import TypeVar, Generic, List

from sqlalchemy.orm import Session, Query

T = TypeVar('T')


class ReadWriteRepository(Generic[T]):
    def __init__(self, entity: T):
        self.entity = entity

    def save(self, entity: T, db: Session):
        db.add(entity)
        db.commit()
        return entity

    def get_all(self, db: Session) -> List[T]:
        entities: List[T] = db.query(self.entity).all()
        return entities

    def get_by_id(self, id: int, db: Session):
        entity: T = db.query(self.entity).filter_by(id=id).first()
        return entity

    def update(self, entity_schema_update, db: Session):
        entity_query: Query = db.query(self.entity).filter_by(id=entity_schema_update.id)
        entity_query.update(entity_schema_update.dict(exclude={'created_at', 'updated_at'}), synchronize_session=False)
        db.commit()
        return entity_query.first()

    def delete(self, id: int, db: Session):
        user_query: Query = db.query(self.entity).filter_by(id=id)
        user_query.delete(synchronize_session=False)
        db.commit()
