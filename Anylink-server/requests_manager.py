import os
import hashlib
import pickle
import threading
import logging
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
        self.scan = False
        self.scan_thread = threading.Thread(target=self._scanning_loop)
        self.transports = {}

    def start_scanning(self):
        self.scan = True
        self.scan_thread.start()
    def stop_scanning(self):
        self.scan = False
    def _scanning_loop(self):
        while self.scan:
            self.transports = self.handler_class.users
    def accept_user_clients(self,user):
        for trans,email in self.transports.items():
            if email == user:
                channel = trans.accept(timeout=1)
                if channel is not None:
                    self._initiate_channel(channel,email)



    def _initiate_channel(self,channel,email):
        data = channel.recv(40)
        data = data.decode("utf-8")
        logging.debug("Data recived: {data}".format(data=data))
        if data == self.READY:
            channel.send(self.CONFIRM_READY)
            self.channels[channel] = email
        else:
            channel.close()

    def _create_channel(self,user):
        self.channels[user] = self.handler_class.users[user].accept()
        data = self.channels[user].recv(40)
        data = data.decode("utf-8")
        logging.debug("Data recived: {data}".format(data=data))
        if data == self.READY:
            self.channels[user].send(self.CONFIRM_READY)
        else:
            self.channels[user].close()
            del self.channels[user]

    def get_user_channels(self,email):
        uchans = []
        logging.debug("Current user channels: {data}".format(data=self.channels))
        for chan in self.channels:
            if not chan.get_transport().active:
                chan.get_transport().close()
            if self.channels[chan] == email:
                uchans.append(chan)
        return uchans



    def send_file(self,chan,file_path):
        chan.send(self.SEND_FILE)
        size = str(len(file_path))
        size += '.' * int((64 - len(size)))
        chan.send(str(size))
        chan.send(file_path)
        size = chan.recv(64)
        size = size.decode('utf-8')
        size = size.replace('.','')
        msg = chan.recv(int(size))
        msg = msg.decode('utf-8')
        logging.debug("Message recived: {msg}".format(msg=msg))
        if msg == "finishfile":
            return True

        return False

    def send_tree(self,chan,path):

        chan.send(self.SEND_TREE)
        logging.debug("TREE:tree request sent")
        size = len(path)
        size = str(size)
        size += '.' * int((64 - len(size)))
        chan.send(str(size))
        logging.debug("TREE:tree size sent")
        chan.send(path)
        logging.debug("TREE:tree path sent")
        logging.debug("TREE:waiting for size")
        size = chan.recv(64)
        logging.debug("TREE:got size")
        size = size.decode('utf-8')
        size = size.replace('.','')
        logging.debug("TREE:wating for tree")
        raw_tree = chan.recv(int(size))
        logging.debug("TREE:got tree")
        dirs,files = pickle.loads(raw_tree)
        return dirs,files

