print("importing...")
from conf import Configuration
from server import AnylinkServer

def main():
    print("config...")
    config = Configuration("config.ini")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_address, config = config)
    print("serving...")
    server.serve_forever()

if __name__ == "__main__":
    main()