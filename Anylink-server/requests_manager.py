import os
import hashlib
import threading
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
        self.scan_thread = threading.Thread(target=self._scanning_loop())
    def start_scanning(self):
        self.scan_thread.start()
    def _scanning_loop(self):
        while True:
            self.transports = self.handler_class.users
    def accept_user_clients(self,user):
        for trans,email in self.transports.items():
            if email == user:
                channel = trans.accept()
                self._initiate_channel(channel,email)


    def _initiate_channel(self,channel,email):
        data = channel.recv(40)
        data = data.decode("utf-8")
        print(data)
        if data == self.READY:
            self.channel.send(self.CONFIRM_READY)
            self.channels[channel] = email
        else:
            channel.close()

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
                data = self.channels[user].recv(56).decode("utf-8")
                if data == self.KEY_SENT:
                    with open("/{email_hash}/storage/key".format(email_hash = email_hash),"rb") as f:
                        raw_key = f.read()
                    with open("/{email_hash}/ssh/authorized_keys".format(email_hash = email_hash),"wb+") as f:
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
