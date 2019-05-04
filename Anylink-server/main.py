print("importing...")
from config import Configuration
from server import AnylinkServer,SFTPHandler
import threading
from requests_manager import RequestsManager
import readchar

def main():
    print("config...")
    config = Configuration("/home/orikeidar01/config.json","anylink")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    print("serving...")
    sftp_thread = threading.Thread(target=server.serve_forever)
    sftp_thread.start()

    requests_manager = RequestsManager(SFTPHandler)
    while True:
        print("select action:")
        print("1) view connected users")
        print("2) open channel with a user")
        print("3) obtain file from user")
        char = None
        while char is None or (char!='1' and char!='2' and char!='3'):
            char = readchar.readkey()

        if char == '1':
            for u in requests_manager.channels:
                print(u)
        if char == '2':
            user = input("enter user email: ")
            requests_manager.get_channel(user)
        if char == '3':
            user = input("enter user email: ")
            requests_manager.get_channel(user)
            path = input("enter file path: ")
            requests_manager.send_file(user,path)





if __name__ == "__main__":
    main()