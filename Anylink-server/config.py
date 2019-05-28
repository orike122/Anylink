import json
from database import Database
import paramiko


class Configuration():
    """Configuration class for loading configurations"""
    def __init__(self,json_path: str,configuration: str):
        """
        C'tor for Configuration object
        :param json_path: Path to json configuration file
        :param configuration: Name of configuration set
        """
        self.json_path = json_path
        self.conf = configuration
        self.load()

    def load(self):
        """Loads host keys and database"""
        with open(self.json_path,"r") as json_file:
            json_handle = json.load(json_file)
            listen_port = json_handle[self.conf]["listen_port"]
            self.bind_addr = ("0.0.0.0",listen_port)
            host_key_path = json_handle[self.conf]["host_key_path"]
            self.host_keys = [paramiko.RSAKey.from_private_key_file(filename=host_key_path)]
            self.database = Database(json_handle[self.conf]["database_path"])



