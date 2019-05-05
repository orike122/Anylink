import base64

import paramiko
import crypt
class Authorization(paramiko.ServerInterface):


    def __init__(self, database, set_auth_method):
        self.database = database
        self.database.set_default_table("anylink")
        self._set_auth_method = set_auth_method

    def get_allowed_auths(self, email):
        return "publickey,password"

    def check_auth_none(self, email):
        return paramiko.AUTH_FAILED

    def check_auth_password(self, email, password):
        user = self.database.search_database(email)
        if user is not None:
            print("user in records...")
            pwhash = user["password_hash"]
            if crypt.crypt(password, pwhash) != pwhash:
                print("user passwd is wrong...")
                return paramiko.AUTH_FAILED
        else:
            print("user not in records...")
            return paramiko.AUTH_FAILED
        print("user auth successful...")
        self._set_auth_method(user)
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, email, key):
        print("check key....")
        user = self.database.search_database(email)
        if user is not None:
            print("get keys....")
            auth_keys = self._get_auth_keys(user)
            if key in auth_keys:
                print("set user....")
                self._set_auth_method(user)
                print("succ....")
                return paramiko.AUTH_SUCCESSFUL
        print("fail....")
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def _get_auth_keys(self,user):
        authorized_keys = []
        filename = "/{email_hash}/ssh/authorized_keys".format(email_hash = user["email_hash"])
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
                    k = paramiko.RSAKey(data=base64.decodestring(d))
                else:
                    k = paramiko.DSSKey(data=base64.decodestring(d))
                del d
                authorized_keys.append(k)
        return authorized_keys
