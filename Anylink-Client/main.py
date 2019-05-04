from client import Client
import json
import os
def main():
    with open("config.json","r") as f:
        json_handle = json.load(f)
        ip = json_handle["ip"]
        port = json_handle["port"]
        if "auth_keys_path" in json_handle:
            auth_keys_path = json_handle["auth_keys_path"]
        else:
            auth_keys_path = None

    if auth_keys_path is None:
        print("begin ssh-key generation process.........")
        os.system("ssh-keygen")
        auth_keys_path = input("insert path of public ssh key: ")
        with open("config.json", "r") as f:
            json_handle = json.load(f)
            json_handle["auth_keys_path"] = auth_keys_path
        with open("config.json", "w") as f:
            json.dump(json_handle,f)

        client = Client((ip, port))
        email = input("enter email:")
        passwd = input("enter email:")
        client.connect(email,passwd)
    else:
        print("welcome again............")
        client = Client((ip, port),auth_keys_path)
        email = input("enter email:")
        client.connect(email)

    client.start_client()
if __name__ == "__main__":
    main()