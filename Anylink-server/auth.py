import base64
import paramiko
import logging
from database import Database
import types
import typing


class Authorization(paramiko.ServerInterface):
    """Class for authorizing SFTP requests"""

    def __init__(self, database: Database, set_auth_method: types.FunctionType):
        """
        C'tor for Authorization class
        :param database: Database object used to manage the database
        :param set_auth_method: Function that gives authorization functionality
        """
        self.database = database
        self.database.set_default_table("anylink")
        self._set_auth_method = set_auth_method

    def get_allowed_auths(self, email: str) -> types.Tuple:
        """
        Return a tuple that contains allowed auth methods
        :param email: User's email
        :return: a tuple that contains allowed auth methods
        """
        return "publickey,password"

    def check_auth_none(self, email: str) -> int:
        """
        Trys to authorized with no auth
        :param email: User's email
        :return: paramiko's Auth code
        """
        return paramiko.AUTH_FAILED

    def check_auth_password(self, email: str, password: str) -> int:
        """
        Trys to authorized with password auth
        :param email: User's email
        :param password: User's password hash
        :return: paramiko's Auth code
        """
        user = self.database.search_database(email)
        if user is not None:
            logging.info("User's email is valid: {user}".format(user=email))
            pwhash = user["password_hash"]
            if password.lower() == pwhash.lower():
                logging.info("Failed to auhenticate user: {user}".format(user=email))
                return paramiko.AUTH_FAILED
        else:
            logging.info("User's email is not valid: {user}".format(user=email))
            return paramiko.AUTH_FAILED
        logging.info("User successfully authenticated: {user}".format(user=email))
        self._set_auth_method(user)
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, email: str, key: str) -> int:
        """
        Trys to authorized with publickey auth
        :param email: User's email
        :param key: User's key
        :return: paramiko's Auth code
        """
        user = self.database.search_database(email)
        if user is not None:
            auth_keys = Authorization._get_auth_keys(user)
            if key in auth_keys:
                self._set_auth_method(user)
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    @staticmethod
    def _get_auth_keys(user: str) -> typing.List[paramiko.PKey]:
        """
        Returns a list of user's public keys
        :param user: user's email
        :return: a list of user's public keys
        """
        authorized_keys = []
        filename = "/{email_hash}/ssh/authorized_keys".format(email_hash=user["email_hash"])
        for rawline in open(filename, 'r'):
            line = rawline.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("ssh-rsa ") or line.startswith("ssh-dss "):
                # Get the key field
                try:
                    d = " ".join(line.split(" ")[1:]).lstrip().split(" ")[0]
                except:
                    # Parse error
                    continue
                if line.startswith("ssh-rsa"):
                    d = d.encode()
                    k = paramiko.RSAKey(data=base64.decodestring(d))
                else:
                    d = d.encode()
                    k = paramiko.DSSKey(data=base64.decodestring(d))
                del d
                authorized_keys.append(k)
        return authorized_keys
