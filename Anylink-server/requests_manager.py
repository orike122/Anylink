
class RequestsManager():
    users ={}

    @staticmethod
    def add_transport(transport,user):
        RequestsManager.users[user["email"]] = transport
