from passlib.context import CryptContext


class HashPassword:
    """This class consists of 2 methods to encrypt the users password for storage, as well as
    verify that the encryption is correct.
    """

    def __init__(self) -> None:
        """Initializes the private crypt_context attribute to the desired encryption and defaults 
        to the next available encryption in case of deprecation.
        """
        self.__crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_hashed_password(self, password: str) -> str:
        """This method takes the users password and returns it encrypted.
        Args:
            password (str): Password to encrypt in plain text format.
        Returns:
            str: Returns initial password argument but encrypted.
        """
        return self.__crypt_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """This method verifies that the users password was properly encrypted.
        Args:
            password (str): Password to encrypt in plain text format.
            hashed_password (str): Encrypted password as returned by get_hashed_password method.
        Returns:
            bool: Returns True if the encrypted password equals to the plain text one once decrypted.
        """
        return self.__crypt_context.verify(password, hashed_password)
