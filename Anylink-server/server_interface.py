import paramiko
import sys
import os
import posixpath
import logging
from socketserver import ThreadingTCPServer
import types
import typing
import io

class SFTPServerInterface(paramiko.SFTPServerInterface):
    """
    SFTP Server Interface, class that overrides
    function that gives access to the file system
    """
    def __init__(self, server: ThreadingTCPServer,get_user_method: types.FunctionType):
        """
        C'tor for SFTP Server Interface
        :param server: sftp server
        :param get_user_method:
        """
        self.server = server
        # magic string for base dir generated from email hash
        self._base_dir = "/{email_hash}/storage".format(
            email_hash = get_user_method()["email_hash"])

    def _local_path(self, sftp_path: str) -> str:
        """
        Returns local path equivalent of remote path
        :param sftp_path: remote path
        :return: local path equivalent of remote path
        """
        if sys.platform == 'win32':
            # raise not implemented in case trying to use on Windows
            raise NotImplementedError("win32 not implemented")

        # transforming relative path to an absolute path
        absolute_base_path = os.path.abspath(self._base_dir)
        # validate path structure
        if not sftp_path.startswith("/"):
            raise ValueError("Invalid SFTP path {path}".format(path=sftp_path))

        # normalizeing an stripping path for assertions
        sp = posixpath.normpath(sftp_path)
        sp = sp.lstrip("/")
        assert ('..' not in posixpath.split(sp))
        lp = os.path.abspath(os.path.join(self._base_dir, sp))
        assert (os.path.commonprefix((absolute_base_path, lp)) == absolute_base_path)
        return lp

    def list_folder(self,sftp_path: str) -> typing.List[paramiko.SFTPAttributes]:
        """
        List folder's content
        :param sftp_path: remote path
        :return: list of elements in folder
        """
        local_path = self._local_path(sftp_path) # convert path
        retval = []
        for fname in os.listdir(local_path):
            fpath = os.path.join(local_path,fname)
            retval.append(paramiko.SFTPAttributes.from_stat(os.lstat(fpath),fname))
        return retval

    def stat(self, sftp_path: str) -> paramiko.SFTPAttributes:
        """
        Returns SFTPAttributes for an object in specific path with symlink
        :param sftp_path: remote path
        :return: SFTPAttributes for an object in specific path
        """
        local_path = self._local_path(sftp_path)# convert path
        fname = os.path.basename(local_path) # extract file name
        return paramiko.SFTPAttributes.from_stat(os.stat(local_path),fname)

    def lstat(self, sftp_path: str) -> paramiko.SFTPAttributes:
        """
        Returns SFTPAttributes for an object in specific path without symlink
        :param sftp_path: remote path
        :return: SFTPAttributes for an object in specific path
        """
        local_path = self._local_path(sftp_path)# convert path
        fname = os.path.basename(local_path)# extract file name
        return paramiko.SFTPAttributes.from_stat(os.lstat(local_path), fname)

    def open(self, sftp_path: str, flags: int, attr: paramiko.SFTPAttributes) -> io.TextIOWrapper:
        """
        Opens a file with given remote
        :param sftp_path: Remote path
        :param flags: os open mode file flags
        :param attr: SFTP file attributes
        :return: file handle object
        """
        local_path = self._local_path(sftp_path)
        handle = paramiko.SFTPHandle()
        readfile = None
        writefile = None
        # convert os flags to file handles with python str flags
        if flags & os.O_WRONLY:
            writefile = open(local_path, "wb")

        elif flags & os.O_RDWR:
            readfile = open(local_path, "rb")
            writefile = open(local_path, "wb")
        else:
            readfile = open(local_path,"rb")

        handle.readfile = readfile
        handle.writefile = writefile
        logging.info("File was opened in: {path}".format(path=local_path))
        return handle

