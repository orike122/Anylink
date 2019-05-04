print("importing...")
from config import Configuration
from server import AnylinkServer
import threading
from requests_manager import RequestsManager
import time

def main():
    print("config...")
    config = Configuration("/home/orikeidar01/config.json","anylink")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    print("serving...")
    sftp_thread = threading.Thread(target=server.serve_forever)
    sftp_thread.start()
    time.sleep(10)
    testusr=RequestsManager.users["testusr@gmail.com"]
    testusr.accept()


if __name__ == "__main__":
    main()