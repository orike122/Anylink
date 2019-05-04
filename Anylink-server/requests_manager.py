
class RequestsManager():
    def __init__(self,handler_class):
        self.handler_class = handler_class
        self.channels = {}
    def _create_channel(self,user):
        self.channels[user] = self.handler_class.users[user].accept()

    def get_channel(self,user):
        if user in self.channels:
            return self.channels[user]
        elif user in self.handler_class.users:
            self._create_channel(user)
            return self.channels[user]
        return None

    def send_file(self,user,file_path):
        self.channels[user].send("sendfile,{file_path}".format(file_path= file_path))
