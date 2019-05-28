import socketserver
import paramiko
from auth import Authorization
from server_interface import SFTPServerInterface
from config import Configuration
from socket import socket
import logging
import typing


class AnylinkServer(socketserver.ThreadingTCPServer):
    """Anylink Server, implementing a threading tcp server for SFTP"""

    def __init__(self, addr: typing.Tuple[str, int], config: Configuration):
        """
        C'tor for Anylink Server, threading tcp server for SFTP file transfer
        :param addr: server's bind address
        :param config: configuration object for server
        """
        self.allow_reuse_address = True
        super().__init__(addr, SFTPHandler)

        self.database = config.database
        self.host_keys = config.host_keys


class SFTPHandler(socketserver.BaseRequestHandler):
    """Handler class for Anylink Server connections"""
    TIMEOUT = 120  # timeout for request
    users = {}  # dict of transport user

    def setup(self):
        """Override of setup function"""
        self.transport = self.make_transport(self.request)
        self.load_server_moduli()
        self.set_security_options()
        self.add_host_keys()
        self.set_subsystem_handlers()

    def handle(self):
        """Override of handle function"""
        server_interface = Authorization(self.server.database, self._set_auth_user)
        self.transport.start_server(server=server_interface)
        channel = self.transport.accept(self.TIMEOUT)
        logging.info("new connection from: {addr}".format(addr=channel.getpeername()))
        SFTPHandler.users[self.transport] = self._get_auth_user()["email"]
        if channel is None:
            logging.info("connection faild :(")
            raise Exception("session channel not opened (auth failed?)")
        self.transport.join()

    def finish(self):
        """Override of finish function"""
        del SFTPHandler.users[self.transport]

    def _set_auth_user(self, user: dict):
        """
        Sets the authorized user
        :param user: user info dict from database
        """
        self._auth_user = user

    def _get_auth_user(self) -> typing.Dict[str, str]:
        """
        returns the authorized user
        :return: authorized user
        """
        return self._auth_user

    def make_transport(self, sock: socket) -> paramiko.Transport:
        """
        Creates an SSH transport between the server and the client over a given socket
        :param sock: socket on which to create the transport
        :return: SSH trnasport
        """
        return paramiko.Transport(sock)

    def load_server_moduli(self):
        """Load server moduli for request's transport, for key negotiation"""
        self.transport.load_server_moduli()

    def set_security_options(self):
        """Sets security options for request's transport"""
        sec_options = self.transport.get_security_options()

        sec_options.digests = ('hmac-sha1',)

        sec_options.compression = ('zlib@openssh.com', 'none')

    def add_host_keys(self):
        """Add host keys to the request's transport"""
        for key in self.server.host_keys:
            self.transport.add_server_key(key)

    def set_subsystem_handlers(self):
        """Sets an sftp subsystem handler"""
        self.transport.set_subsystem_handler('sftp', paramiko.SFTPServer,
                                             sftp_si=SFTPServerInterface, get_user_method=self._get_auth_user)
