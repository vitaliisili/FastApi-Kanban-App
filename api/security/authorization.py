from typing import List, Set
from fastapi import Depends, HTTPException, status
from api.models.user_model import User
from api.security.jwt_config import get_principal


class SecurityRole:
    """ Represents a security role for authorization check for request.

    SecurityRole is used to check if user has permission to access specific resources by role.
    SecurityRole is callable that mean it can be used as dependency injection, use FastApi Depends()
    to inject SecurityRole,
    """

    def __init__(self, required_roles: List[str], exact: bool = False):
        """ Initialize SecurityRole class

        The required_roles argument get a list of role name that authenticated user must contain for accessing specific
        resources.

        The 'exact' argument get a boolean that indicates user must contain all provided roles in 'role_requirement'
        list, if user roles not contain all provided roles the exception will be risen.
        The exact argument be default is set to false that mean if user has at least one role that is indicated
        in role_requirement list user will be able to access the specific resources.

        Parameters:
            required_roles (List[str]): A list of required roles.
            exact (bool, optional): Specifies if all roles in required_role list should be present in user roles.
                                    By Defaults is set to False.
        Raises:
            ValueError: If required_role list is empty
            TypeError: If role provided to required_role list are not of type str or 'exact'
        """
        if not required_roles:
            raise ValueError("Required roles list must contain at least one role")

        if not all(isinstance(role, str) for role in required_roles):
            raise TypeError("Unsupported type: accept only list of string")

        if not isinstance(exact, bool):
            raise TypeError(f"Unsupported type: {type(exact)}, accept only boolean")

        self.required_roles: Set[str] = set(role.upper() for role in required_roles)
        self.exact = exact

    def __call__(self, authenticated_user: User = Depends(get_principal)):
        """ Callable method for authorization check.
        Parameters:
            authenticated_user (User): authenticated user who try to access secured resources
        Raises:
            HTTPException: If user not contain specific roles
        """
        authenticated_user_roles: Set[str] = {role.name.upper() for role in authenticated_user.roles}
        role_interception: Set[str] = self.required_roles.intersection(authenticated_user_roles)

        forbidden_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                            detail="Forbidden: Access is denied")

        if self.exact and role_interception != self.required_roles:
            raise forbidden_exception
        elif not role_interception:
            raise forbidden_exception
