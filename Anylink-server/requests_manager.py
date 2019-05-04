import select
class RequestsManager():
    READY = "ready"
    CONFIRM_READY = "confready"
    SEND_KEY = "sendkey"
    SEND_FILE = "sendfile"
    SEND_TREE = "sendtree"
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
            data = self.channels[user].send(self.CONFIRM_READY)
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
        self.channels[user].send(size)
        self.channels[user].send(file_path)
