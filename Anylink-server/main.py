from conf import Configuration
from server import AnylinkServer

def main():
    config = Configuration("config.ini")
    server = AnylinkServer(config.bind_address, config = config)
    print("serving...")
    server.serve_forever()

if __name__ == "__main__":
    main()