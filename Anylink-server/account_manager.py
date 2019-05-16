
import hashlib
import os
class AccountManager():

    def __init__(self,database):
        self.database = database
    @staticmethod
    def _create_dir_structure(email_hash):
        main_dir = "/{email_hash}".format(email_hash=email_hash)
        ssh_dir = "/{email_hash}/ssh".format(email_hash=email_hash)
        storage_dir = "/{email_hash}/storage".format(email_hash=email_hash)

        os.mkdir(main_dir)
        os.mkdir(ssh_dir)
        os.mkdir(storage_dir)
        open('/{email_hash}/ssh/authorized_keys'.format(email_hash=email_hash), 'a').close()
    def create_user(self,email,passwordh):
        res = self.database.search_database(email)
        if res is None:
            self.database.add_user(email,passwordh)
            user = self.database.search_database(email)
            self._create_dir_structure(user["email_hash"])
            return True
        return False
    def validate_user(self,email,password):
        res = self.database.search_database(email)
        if res is not None and res["password_hash"].lower() == password.lower():
            return True
        else:
            return False


