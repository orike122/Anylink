import socketserver
import paramiko
from auth import Authorization
from server_interface import SFTPServerInterface
from requests_manager import RequestsManager

class AnylinkServer(socketserver.ThreadingTCPServer):

    def __init__(self,addr,config):
        print("super initialize server...")
        self.allow_reuse_address = True
        super().__init__(addr,SFTPHandler)

        self.database = config.database
        self.host_keys = config.host_keys


class SFTPHandler(socketserver.BaseRequestHandler):

    TIMEOUT = 120
    users  = {}
    def setup(self):
        self.transport = self.make_transport(self.request)
        self.load_server_moduli()
        self.set_security_options()
        self.add_host_keys()
        self.set_subsystem_handlers()

    def handle(self):
        server_interface = Authorization(self.server.database, self._set_auth_user)
        self.transport.start_server(server=server_interface)
        channel = self.transport.accept(self.TIMEOUT)
        SFTPHandler.users[self.transport] = self._get_auth_user()["email"]
        print(channel)
        if channel is None:
            raise Exception("session channel not opened (auth failed?)")
        self.transport.join()
    def finish(self):
        del SFTPHandler.users[self.transport]

    def _set_auth_user(self,user):
        self._auth_user = user

    def _get_auth_user(self):
        return self._auth_user

    def make_transport(self,sock):
        return paramiko.Transport(sock)

    def load_server_moduli(self):
        self.transport.load_server_moduli()

    def set_security_options(self):
        sec_options = self.transport.get_security_options()

        sec_options.digests = ('hmac-sha1',)

        sec_options.compression = ('zlib@openssh.com','none')

    def add_host_keys(self):
        for key in self.server.host_keys:
            self.transport.add_server_key(key)

    def set_subsystem_handlers(self):
        self.transport.set_subsystem_handler('sftp', paramiko.SFTPServer,
            sftp_si = SFTPServerInterface, get_user_method = self._get_auth_user)
