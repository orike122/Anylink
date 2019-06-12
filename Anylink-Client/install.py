import argparse
import logging
def install_gui():
    pass

def install_client():
    pass
def init_registers():
    pass
if __name__ == "__main__":
    logging.basicConfig(level=logging.info())
    parser = argparse.ArgumentParser(description='Create program path')
    parser.add_argument('--path',metavar='<PATH>',type=str,nargs='+',help="a path for program installation")
    args = parser.parse_args(['--path','path'])
    path = args.path
    logging.info("Installing GUI program.....")
    install_gui()
    logging.info("Installing client.....")
    install_client()
    logging.info("Set up registers.....")
    init_registers()

