from client import Client
import json
import os
def main():
    with open("config.json","r") as f:
        json_handle = json.load(f)
        ip = json_handle["ip"]
        port = json_handle["port"]
    client = Client((ip, port))
    email = input("enter email:")
    passwd = input("enter password:")
    client.connect(email,passwd)

    client.start_client()
if __name__ == "__main__":
    main()