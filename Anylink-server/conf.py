import paramiko
import configparser
import base64
class User():
    def __init__(self):
        self.anonymous = False
        self.root_path = None
        self.authorixed_keys = []

class Configuration():

    def __init__(self, conffile_path):
        self.conffile_path = conffile_path
        self.load()

    def load(self):
        cfgSection = 'anylink'

        # Read the main configuration file
        config = configparser.RawConfigParser()
        if not config.read(self.conffile_path):
            raise Exception("Unable to load configuration file %r" % (self.conffile_path,))

        # Read bind address
        listen_host = config.get(cfgSection, 'listen_host')
        listen_port = config.getint(cfgSection, 'listen_port')
        self.bind_address = (listen_host, listen_port)

        # Load host keys
        host_keys = []
        for optname in config.options(cfgSection):
            if optname != "host_key" and not optname.startswith("host_key."):
                continue
            filename = config.get(cfgSection, optname)
            try:
                host_key = paramiko.RSAKey.from_private_key_file(filename=filename)
            except paramiko.SSHException:
                host_key = paramiko.DSSKey.from_private_key_file(filename=filename)
            host_keys.append(host_key)
            host_key = None  # erase reference to host key
        if not host_keys:
            raise Exception("config file %r does not specify any host key" % (self.conffile_path,))
        self.host_keys = host_keys

        # Load the user auth file (authconfig.ini)
        auth_config = configparser.RawConfigParser()
        auth_config.read(config.get(cfgSection, 'auth_config'))
        users = {}
        for username in auth_config.sections():
            u = User()
            if auth_config.has_option(username, 'anonymous'):
                u.anonymous = auth_config.getboolean(username, 'anonymous')
            if not u.anonymous:
                u.password_hash = auth_config.get(username, 'password')
            u.root_path = auth_config.get(username, 'root_path')

            # TODO: Move authorized_keys parsing into a separate function
            u.authorized_keys = []
            if auth_config.has_option(username, 'authorized_keys_file'):
                filename = auth_config.get(username, 'authorized_keys_file')
                for rawline in open(filename, 'r'):
                    line = rawline.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("ssh-rsa ") or line.startswith("ssh-dss "):
                        # Get the key field
                        try:
                            d = " ".join(line.split(" ")[1:]).lstrip().split(" ")[0]
                        except:
                            # Parse error
                            continue
                        if line.startswith("ssh-rsa"):
                            k = paramiko.RSAKey(data=base64.decodestring(d))
                        else:
                            k = paramiko.DSSKey(data=base64.decodestring(d))
                        del d
                        u.authorized_keys.append(k)
            users[username] = u
            self.users = users