import argparse
import logging
import os
import winreg

def install_gui(path):
    try:
        os.mkdir(path)
        os.system(r'mv anylinkInit.exe {path}'.format(path=path))
    except EnvironmentError as e:
        logging.fatal("Error while installin GUI :(")
        raise e

def install_client(path):
    try:
        os.system(r'mv client.py {path}'.format(path=path))
        os.system(r'mv main.py {path}'.format(path=path))
        os.mkdir(os.path.join(path,'ssh'))
    except EnvironmentError as e:
        logging.fatal("Error while installing client :( ")
        raise e

def init_registers(path):
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    try:
        winreg.CreateKey(reg, r'SOFTWARE\Anylink')
    except EnvironmentError as e:
        logging.fatal("Error while creating Anylink's registry key :(")
        raise e

    key = winreg.OpenKey(reg, r'SOFTWARE\Anylink')
    try:
        winreg.SetValueEx(key,'key_path', 0, winreg.REG_SZ, os.path.join(path,'ssh'))
        winreg.SetValueEx(key, 'has_init', 0, winreg.REG_DWORD, 0)
    except EnvironmentError as e:
        logging.fatal("Error while setting value :( ")
        raise e
    finally:
        winreg.CloseKey(key)

if __name__ == "__main__":
    logging.basicConfig(level=logging.info())
    parser = argparse.ArgumentParser(description='Create program path')
    parser.add_argument('--path',metavar='<PATH>',type=str,nargs='+',help="a path for program installation")
    args = parser.parse_args(['--path','path'])
    path = args.path
    logging.info("Installing GUI program.....")
    err = install_gui()
    logging.info("Installing client.....")
    install_client()
    logging.info("Set up registers.....")
    init_registers()

