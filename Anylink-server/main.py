print("importing...")
from config import Configuration
from server import AnylinkServer
import threading

def main():
    print("config...")
    config = Configuration("/home/orikeidar01/config.json","anylink")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    print("serving...")
    sftp_thread = threading.Thread(target=server.serve_forever)
    sftp_thread.start()
    

if __name__ == "__main__":
    main()