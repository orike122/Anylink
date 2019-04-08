import paramiko
import sys
import os
import posixpath
import server

class SFTPServerInterface(paramiko.SFTPServerInterface):

    def __init__(self, server,get_user_method):
        self._base_dir = get_user_method().root_path

    def _local_path(self, sftp_path):
        if sys.platform == 'win32':
            #TODO implement for win32
            raise NotImplementedError("win32 not implemented")

        absolute_base_path = os.path.abspath(self._base_dir)
        if not sftp_path.startswith("/"):
            raise ValueError("Invalid SFTP path {path}".format(path=sftp_path))

        #TODO go through this piece of code
        sp = posixpath.normpath(sftp_path)
        sp = sp.lstrip("/")
        assert ('..' not in posixpath.split(sp))
        lp = os.path.abspath(os.path.join(self._base_dir, sp))
        assert (os.path.commonprefix((absolute_base_path, lp)) == absolute_base_path)
        return lp

    def list_folder(self,sftp_path):
        local_path = self._local_path(sftp_path)
        retval = []
        for fname in os.listdir(local_path):
            fpath = os.path.join(local_path,fname)
            retval.append(paramiko.SFTPAttributes.from_stat(os.lstat(fpath),fname))
        return retval

    def stat(self, sftp_path):
        local_path = self._local_path(sftp_path)
        fname = os.path.basename(local_path)
        return paramiko.SFTPAttributes.from_stat(os.stat(local_path),fname)

    def lstat(self, sftp_path):
        local_path = self._local_path(sftp_path)
        fname = os.path.basename(local_path)
        return paramiko.SFTPAttributes.from_stat(os.lstat(local_path), fname)

    def open(self, sftp_path, flags, attr):
        local_path = self._local_path(sftp_path)
        print(local_path)
        handle = paramiko.SFTPHandle()
        readfile = None
        writefile = None
        if flags & os.O_RDONLY:
            readfile = open(local_path,"rb")
        if flags & os.O_WRONLY:
            writefile = open(local_path, "wb")
        if flags & os.O_RDWR:
            readfile = open(local_path, "rb")
            writefile = open(local_path, "wb")
        handle.readfile = readfile
        handle.writefile = writefile

        print("open....")
        return handle

