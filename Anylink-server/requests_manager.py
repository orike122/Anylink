import os
import hashlib
class RequestsManager():
    READY = "ready"
    CONFIRM_READY = "confready"
    SEND_KEY = "sendkey"
    SEND_FILE = "sendfile"
    SEND_TREE = "sendtree"
    KEY_SENT = "keysent"
    def __init__(self,handler_class):
        self.handler_class = handler_class
        self.channels = {}
        self.ready = {}
    def _create_channel(self,user):
        self.channels[user] = self.handler_class.users[user].accept()
        data = self.channels[user].recv(40)
        data = data.decode("utf-8")
        print(data)
        if data == self.READY:
            self.channels[user].send(self.CONFIRM_READY)
            email_hash = hashlib.sha256(user.encode("utf-8")).hexdigest()
            if not os.path.isfile("/{email_hash}/ssh/authorized_keys".format(email_hash = email_hash)):
                self.channels[user].send(self.SEND_KEY)
                data = self.channels[user].recv(56)
                if data == self.KEY_SENT:
                    with open("/{email_hash}/storage/key".format(email_hash = email_hash),"r") as f:
                        raw_key = f.read()
                    with open("/{email_hash}/ssh/authorized_keys".format(email_hash = email_hash),"w+") as f:
                        f.write(raw_key)
                        print("write key")

        else:
            self.channels[user].close()
            del self.channels[user]


    def get_channel(self,user):
        if user in self.channels:
            return self.channels[user]
        elif user in self.handler_class.users:
            self._create_channel(user)
            return self.channels[user]
        return None



    def send_file(self,user,file_path):
        self.channels[user].send(self.SEND_FILE)
        size = len(file_path)*8
        self.channels[user].send(str(size))
        self.channels[user].send(file_path)
