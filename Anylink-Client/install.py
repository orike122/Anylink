import argparse
import logging
import os
import time

def install_gui(path):
    try:
        os.mkdir(path)
        os.system(r'mv anylinkInit.exe {path}'.format(path=path))
    except EnvironmentError:
        logging.fatal("Error while installin GUI :(")
        raise e
    return err

def install_client(path):
    try:
        os.system(r'mv client.py {path}'.format(path=path))
        os.system(r'mv main.py {path}'.format(path=path))
    except EnvironmentError as e:
        logging.fatal("Error while installin GUI :( , exiting.....")
        raise e
def init_registers(path):
    pass

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

