
import paramiko
import crypt
class Authorization(paramiko.ServerInterface):

    users = None

    def __init__(self, users, set_auth_method):
        self.users = users
        self._set_auth_method = set_auth_method

    def get_allowed_auths(self, username):
        return "publickey,password"

    def check_auth_none(self, username):
        return paramiko.AUTH_FAILED

    def check_auth_password(self, username, password):
        if username in self.users:
            pwhash = self.users[username].password_hash
            if crypt.crypt(password, pwhash) != pwhash:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_FAILED
        self._set_auth_method(self.users[username])
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        if username in self.users:
            if key in self.users[username].authorized_keys:
                self._set_auth_method(self.users[username])
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
