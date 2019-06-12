import argparse
import logging
import os
import time

def install_gui(path):
    err = False
    try:
        os.mkdir(path)
        os.system(r'mv anylinkInit.exe {path}'.format(path=path))
    except EnvironmentError:
        err = True
    return err

def install_client(path):
    pass
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
    if err:
        logging.fatal("Error while installin GUI :( , exiting.....")
        time.sleep(5)
        exit()
    logging.info("Installing client.....")
    install_client()
    logging.info("Set up registers.....")
    init_registers()

