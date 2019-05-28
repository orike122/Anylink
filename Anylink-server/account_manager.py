
import os
from database import Database

class AccountManager():
    """AccountManager class, thin wrapper of Database that adds functionality and handles user sign up/ip operations"""

    def __init__(self,database: Database):
        """
        C'tor of AccountManager class
        :param database: Database object
        """
        self.database = database

    @staticmethod
    def _create_dir_structure(email_hash: str):
        """
        Creates user's directories structure
        :param email_hash: User's email
        """
        main_dir = "/{email_hash}".format(email_hash=email_hash)
        ssh_dir = "/{email_hash}/ssh".format(email_hash=email_hash)
        storage_dir = "/{email_hash}/storage".format(email_hash=email_hash)

        os.mkdir(main_dir)
        os.mkdir(ssh_dir)
        os.mkdir(storage_dir)
        open('/{email_hash}/ssh/authorized_keys'.format(email_hash=email_hash), 'a').close()

    def create_user(self,email: str,passwordh: str) -> bool:
        """
        Creates a new user with given email and passowrd hash
        :param email: User's email
        :param passwordh: User's password hash
        :return: Does user creation succeeded
        """
        res = self.database.search_database(email)
        if res is None:
            self.database.add_user(email,passwordh)
            user = self.database.search_database(email)
            self._create_dir_structure(user["email_hash"])
            return True
        return False

    def validate_user(self,email: str,password: str) -> bool:
        """
        Validates user credentials
        :param email: User's email
        :param password: User's password hash
        :return: Does user valid
        """
        res = self.database.search_database(email)
        if res is not None and res["password_hash"].lower() == password.lower():
            return True
        else:
            return False


