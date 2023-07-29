from sqlalchemy.orm import Session
from api.models.role_model import Role
from api.repository.read_write_repository import ReadWriteRepository


class RoleRepository(ReadWriteRepository):
    def get_role_by_name(self, name: str, db: Session) -> Role:
        """ Retrieves a role from the database based on its name.
        Parameters:
            name (str): The name of the role to retrieve.
            db (Session): The database session object.
        Returns:
            Role: The role object retrieved from the database, if found.
        """
        role = db.query(Role).filter_by(name=name).first()
        return role
