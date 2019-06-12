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
    #Configure logging options
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Starting server")

    #Create config object
    config = Configuration("/home/orikeidar01/config.json","anylink")
    config.database.set_default_table("anylink")

    #Initiate SFTP server
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    logging.info("Server is now serving")

    try:
        #Start SFTP server thread
        sftp_thread = threading.Thread(target=server.serve_forever)
        sftp_thread.start()

        #Create managers
        requests_manager = RequestsManager(SFTPHandler)
        account_manager = AccountManager(config.database)
        requests_manager.start_scanning()

        #Inject functions
        setattr(anylink,"get_account_manager",lambda: account_manager)
        setattr(anylink, "get_requests_manager", lambda: requests_manager)

        #Start web server
        anylink.start_website()

    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()

