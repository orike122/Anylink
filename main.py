import sys
sys.path.insert(0, '/home/orikeidar01/Anylink-develop/Anylink-server')
sys.path.insert(0, '/home/orikeidar01/Anylink-develop/Anylink-web')
from config import Configuration
from server import AnylinkServer,SFTPHandler
import threading
from requests_manager import RequestsManager
from account_manager import AccountManager
import anylink
import logging

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Starting server")
    config = Configuration("/home/orikeidar01/config.json","anylink")
    config.database.set_default_table("anylink")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    logging.info("Server is now serving")
    try:
        sftp_thread = threading.Thread(target=server.serve_forever)
        sftp_thread.start()

        requests_manager = RequestsManager(SFTPHandler)
        account_manager = AccountManager(config.database)
        requests_manager.start_scanning()

        setattr(anylink,"get_account_manager",lambda: account_manager)
        setattr(anylink, "get_requests_manager", lambda: requests_manager)

        anylink.start_website(requests_manager,account_manager)
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()

