print("importing...")
from config import Configuration
from server import AnylinkServer

def main():
    print("config...")
    config = Configuration("/home/orikeidar01/config.json","anylink")
    print("initialize server...")
    AnylinkServer.allow_reuse_address = True
    server = AnylinkServer(config.bind_addr, config = config)
    print("serving...")
    server.serve_forever()

if __name__ == "__main__":
    main()