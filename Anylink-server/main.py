print("importing...")
from config import Configuration
from server import AnylinkServer, SFTPHandler
import threading
from requests_manager import RequestsManager
from account_manager import AccountManager
import readchar


def main():
    print("config...")
    config = Configuration("/home/orikeidar01/config.json", "anylink")
    config.database.set_default_table("anylink")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config=config)
    print("serving...")
    sftp_thread = threading.Thread(target=server.serve_forever)
    sftp_thread.start()

    requests_manager = RequestsManager(SFTPHandler)
    account_manager = AccountManager(config.database)
    exit = False
    while not exit:
        print("select action:")
        print("1) view connected users")
        print("2) open channel with a user")
        print("3) obtain file from user")
        print("4) create new user")
        print("^C) exit")
        char = None
        while char is None or (
                char != '1' and char != '2' and char != '3' and char != '4' and char != readchar.key.CTRL_C):
            char = readchar.readkey()

        if char == '1':
            for u in requests_manager.channels:
                print(u)
        elif char == '2':
            user = input("enter user email: ")
            requests_manager.get_channel(user)
        elif char == '3':
            user = input("enter user email: ")
            requests_manager.get_channel(user)
            path = input("enter file path: ")
            requests_manager.send_file(user, path)
        elif char == '4':
            user = input("enter user email: ")
            passwd = input("enter user password: ")
            if account_manager.create_user(user, passwd):
                print("user was succefully created")
            else:
                print("email already exists")
        elif char == readchar.key.CTRL_C:
            exit = True

    server.shutdown()


if __name__ == "__main__":
    main()
