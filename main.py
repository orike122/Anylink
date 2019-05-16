from config import Configuration
from server import AnylinkServer,SFTPHandler
import threading
from requests_manager import RequestsManager
from account_manager import AccountManager
import anylink

def main():
    print("config...")
    config = Configuration("/home/orikeidar01/config.json","anylink")
    config.database.set_default_table("anylink")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    print("serving...")
    sftp_thread = threading.Thread(target=server.serve_forever)
    sftp_thread.start()

    requests_manager = RequestsManager(SFTPHandler)
    account_manager = AccountManager(config.database)
    requests_manager.start_scanning()
    anylink.start_website(requests_manager,account_manager)

