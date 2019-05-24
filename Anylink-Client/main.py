from client import Client
import json
import winreg
import paramiko
def main():
    with open("config.json","r") as f:
        json_handle = json.load(f)
        ip = json_handle["ip"]
        port = json_handle["port"]
    client = Client((ip, port))
    email,pkey_path = read_reg()
    pkey = paramiko.RSAKey.from_private_key_file(pkey_path)
    if email is not None and pkey is not None:
        client.connect(email,pkey)
        client.start_client()
    else:
        pass
        #TODO handle errors

def read_reg():
    email = None
    pkey_path = None
    reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    key = winreg.OpenKey(reg,r'SOFTWARE\Anylink')
    try:
        email = winreg.QueryValueEx(key,'user')[0]
        pkey_path = winreg.QueryValueEx(key,'key_path')[0]
    except EnvironmentError as e:
        print(e)
    finally:
        winreg.CloseKey(key)
    return email,pkey_path

if __name__ == "__main__":
    main()