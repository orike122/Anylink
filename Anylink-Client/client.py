import paramiko
"""
protocol:
Client -> Server: "ready"
Client -> Server: "confready"
Server -> Client: "sendkey"
Client -> Server: <<key>>
Server -> Client: "sendfile"
Server -> Client: <<size>>
Server -> Client: <<path>>
Server -> Client: "sendtree"
Client -> Server: <<size>>
Client -> Server: <<tree>>
"""


class Client():
    READY = "ready"
    CONFIRM_READY = "confready"
    SEND_KEY = "sendkey"
    SEND_FILE = "sendfile"
    SEND_TREE = "sendtree"
    LISTEN_PACKET_SIZE = 72

    NOT_CONNECTED = 0
    WAITING_FOR_SFTP_CONNECTION = 1
    WAITING_FOR_CONTROL_CONNECTION = 2
    CONNECTED = 3
    def __init__(self,server_addr):
        self.transport = paramiko.Transport((server_addr))
        self.status = self.NOT_CONNECTED
    def start_client(self):
        pass
    def _size(self,b):
        return len(b)*8
    def _control_recv(self,size):
        data = self.control_chan.recv(size)
        return data
    def connect(self,email,password):
        self.status = self.WAITING_FOR_SFTP_CONNECTION
        self.transport.connect(username=self.email,password=password)
        self.sftp_client = paramiko.SFTPClient.from_transport(self.transport)
        self.status = self.WAITING_FOR_CONTROL_CONNECTION
        self.control_chan = self.transport.open_session()
        self.control_chan.send(self.READY)
        data = self._control_recv(self._size(self.CONFIRM_READY))
        if data == self.CONFIRM_READY:
            self.status = 3
        else:
            print("control connection failure.............")

    def wait_for_request(self):
        data = self._control_recv(self.LISTEN_PACKET_SIZE)
        if data == self.SEND_KEY:
            self.send_file()
        elif data == self.SEND_TREE:
            self.send_tree()
        elif data == self.SEND_FILE:
            self.send_file()

    def send_key(self):
        pass
    def send_tree(self):
        pass
    def send_file(self):
        pass


