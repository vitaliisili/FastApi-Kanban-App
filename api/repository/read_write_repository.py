from typing import TypeVar, Generic, List

from sqlalchemy.orm import Session, Query

T = TypeVar('T')


class ReadWriteRepository(Generic[T]):
    """
    ReadWriteRepository is a generic class that provides basic CRUD (Create, Read, Update, Delete) operations
    for a given entity in a database using SQLAlchemy.

    Parameters:
        T: Type variable representing the entity type.

    Attributes:
        entity (T): The entity class this repository operates on.
    """

    def __init__(self, entity: T):
        self.entity = entity

    def save(self, entity: T, db: Session) -> T:
        """ Saves the provided entity to the database.

        This method adds the given entity to the current session and commits the transaction to persist it
        into the database.
        Parameters:
            entity (T): The entity object to be saved to the database.
            db (Session): The SQLAlchemy session object to use for the database transaction.
        Returns:
            T: The saved entity object, which may include any autogenerated fields populated by the database.
        Raises:
            SQLAlchemyError: If there is an issue with the database transaction or data integrity.
        """
        db.add(entity)
        db.commit()
        return entity

    def get_all(self, db: Session) -> List[T]:
        """ Retrieves all entities of the specified type from the database.

        This method performs a database query to fetch all entities of the specified type ('T') from the database
        and returns them as a list.
        Parameters:
            db (Session): The SQLAlchemy session object to use for the database query.
        Returns:
            List[T]: A list of entities retrieved from the database.
        Raises:
            SQLAlchemyError: If there is an issue with the database query or data retrieval.
        """
        entities: List[T] = db.query(self.entity).all()
        return entities

    def get_by_id(self, id: int, db: Session) -> T:
        """ Retrieves a single entity by its unique identifier from the database.

        This method performs a database query to fetch a single entity of the specified type ('T') from the database
        based on its unique identifier (id) and returns it.
        Parameters:
            id (int): The unique identifier (primary key) of the entity to retrieve.
            db (Session): The SQLAlchemy session object to use for the database query.
        Returns:
            T: The retrieved entity with the specified id.
        Raises:
            SQLAlchemyError: If there is an issue with the database query or data retrieval.
        """
        entity: T = db.query(self.entity).filter_by(id=id).first()
        return entity

    def update(self, entity_schema_update, db: Session) -> T:
        """ Updates an existing entity in the database with the provided data.

        This method finds an existing entity in the database based on the 'id' attribute of the 'entity_schema_update'
        and updates its fields with the provided data. The 'created_at' and 'updated_at' fields are excluded from
        the update. The method then commits the transaction to persist the changes in the database.
        Parameters:
            entity_schema_update: An instance of the schema representing the updated data for the entity.
                                  Typically, this would be a Pydantic model or a dictionary with updated fields.
            db (Session): The SQLAlchemy session object to use for the database query and transaction.
        Returns:
            T: The updated entity object from the database.
        Raises:
            SQLAlchemyError: If there is an issue with the database query or data update.
        """
        entity_query: Query = db.query(self.entity).filter_by(id=entity_schema_update.id)
        entity_query.update(entity_schema_update.dict(exclude={'created_at', 'updated_at'}), synchronize_session=False)
        db.commit()
        return entity_query.first()

    def delete(self, id: int, db: Session) -> None:
        """ Deletes an entity from the database by its unique identifier (id).

        This method performs a database query to find the entity with the specified 'id'
        and deletes it from the database. The deletion is performed without synchronizing the session to
        improve performance. The method then commits the transaction to apply the deletion to the database.
        Parameters:
            id (int): The unique identifier (primary key) of the entity to be deleted.
            db (Session): The SQLAlchemy session object to use for the database query and transaction.
        Raises:
            SQLAlchemyError: If there is an issue with the database query or data deletion.
        """
        user_query: Query = db.query(self.entity).filter_by(id=id)
        user_query.delete(synchronize_session=False)
        db.commit()
