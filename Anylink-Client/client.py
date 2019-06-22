import paramiko
import os
import pickle
import logging
import typing
import socket

"""
protocol:
Client -> Server: "ready"
Client -> Server: "confready"
Server -> Client: "sendkey"
Server -> Client: "keysent"
Client -> Server: <<key>>
Server -> Client: "sendfile"
Server -> Client: <<size>>
Server -> Client: <<path>>
Client -> Server: <<file>>
Server -> Client: "sendtree"
Server -> Client: <<size>>
Server -> Client: <<path>>
Client -> Server: <<size>>
Client -> Server: <<tree>>
"""


class Client():
    # ----------Constants----------
    READY = "ready"
    CONFIRM_READY = "confready"
    SEND_KEY = "sendkey"
    SEND_FILE = "sendfile"
    SEND_TREE = "sendtree"
    KEY_SENT = "keysent"
    LISTEN_PACKET_SIZE = 72

    # ----------Constants----------

    def __init__(self, server_addr: typing.Tuple[str, int]):
        """
        C'tor for SFTP client object
        :param server_addr: address of the server
        """
        self.transport = paramiko.Transport(server_addr)

    def start_client(self):
        """Starts the client loop operation"""
        while True:
            self.wait_for_request()


    def _control_recv(self, size: int) -> str:
        """
        Preform recv from control chnannel
        :param size: size to recv
        :return: String data recived
        """
        data = self.control_chan.recv(size)
        return data.decode("utf-8")

    def connect(self, email: str, pkey: paramiko.PKey):
        """
        Connect to SFTP server
        :param email: User's email
        :param pkey: Private key
        """
        self.transport.connect(username=email, pkey=pkey)
        self.sftp_client = paramiko.SFTPClient.from_transport(self.transport)

        self.control_chan = self.transport.open_session()
        self.control_chan.send(self.READY)
        name = socket.gethostbyname(socket.gethostname()) + " - " + socket.gethostname()
        self.send_with_size(name)
        data = self._control_recv(len(self.CONFIRM_READY))
        if data == self.CONFIRM_READY:
            logging.debug("connected")
        else:
            logging.debug("connection failed")

    def wait_for_request(self):
        """Waits for a request from the server and than perform actions accordingly"""
        data = self._control_recv(self.LISTEN_PACKET_SIZE)

        if data == self.SEND_TREE:
            self.send_tree()
        elif data == self.SEND_FILE:
            self.send_file()

    def send_with_size(self, s: str):
        """
        Sned's data with its size
        :param s: Data to send
        """
        size = str(len(s))
        size += '.' * int((64 - len(size)))

        self.control_chan.send(str(size))
        self.control_chan.send(s)

    def recv_with_size(self) -> str:
        """
        Revc's data with its size
        :return: Recived data
        """
        size = self.control_chan.recv(64)
        size = size.decode('utf-8')
        size = size.replace('.', '')

        msg = self.control_chan.recv(int(size))

        return msg

    def send_tree(self):
        """Senss file tree to SFTP server"""
        path = self.recv_with_size()
        ls = os.listdir(path)

        dirs = [d for d in ls if os.path.isdir(os.path.join(path, d))]
        files = [f for f in ls if os.path.isfile(os.path.join(path, f))]

        pkl = pickle.dumps((dirs, files))
        self.send_with_size(pkl)



    def send_file(self):
        """Sends file to SFTP server"""
        path = self.recv_with_size().decode('utf-8')
        self.sftp_client.put(path, "/" + path.split("/")[-1])

        self.send_with_size("finishfile")
        logging.info("file sent")
