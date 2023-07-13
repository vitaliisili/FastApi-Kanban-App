class BadRequestException(Exception):
    """
    Description:
    The BadRequestException class is a custom exception that represents a "Bad Request" error.
    It can be raised when there is an issue with the incoming request data, indicating that the
    request cannot be processed due to incorrect or invalid parameters.

    Usage:
    It's recommended to use the BadRequestException in situations where the request data does not meet
    the required criteria or is invalid. This helps to provide clear and informative feedback to the user
    about the nature of the error, allowing them to take appropriate action.
    """
    pass


class EntityNotFoundException(Exception):
    """
    Description:
    The EntityNotFoundError class is a custom exception that represents an "Entity Not Found" exception.
    It can be raised when an entity, such as a user, resource, or object, is not found within the system or database.

    Usage:
    Using the EntityNotFoundException class helps to provide clear and specific feedback to the user when an entity
    they are trying to access or manipulate cannot be found. It allows for better error handling and can assist
    in troubleshooting and debugging efforts.
    """
    pass


class EntityAlreadyExistsException(Exception):
    """
    Description:
    This exception indicates that an entity, such as a user, record, or item, already exists in the system
    and cannot be created or added again.

    Usage:
    The `EntityAlreadyExistsException` can be used in scenarios where you need to handle cases when an entity
    is already present in the system. For example, when creating a new user, if a user with the same email
    address already exists, you can raise this exception to indicate the duplication.
    """
    pass
