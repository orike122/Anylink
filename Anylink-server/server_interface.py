import paramiko
import sys
import os
import posixpath

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
    """
    def open(self, sftp_path, flags, attr):
        local_path = self._local_path(sftp_path)
        print(local_path)
        handle = paramiko.SFTPHandle()
        handle.readfile = open(local_path, "rb")
        handle.writefile = open(local_path, "wb")
        print("open....")
        return handle
    """

    def open(self, path, flags, attr):
        path = self._local_path(path)
        try:
            binary_flag = getattr(os, 'O_BINARY',  0)
            flags |= binary_flag
            mode = getattr(attr, 'st_mode', None)
            if mode is not None:
                fd = os.open(path, flags, mode)
            else:
                # os.open() defaults to 0777 which is
                # an odd default mode for files
                fd = os.open(path, flags, 0o666)
        except OSError as e:
            print(e)
            return paramiko.SFTPServer.convert_errno(e.errno)
        if (flags & os.O_CREAT) and (attr is not None):
            attr._flags &= ~attr.FLAG_PERMISSIONS
            paramiko.SFTPServer.set_file_attr(path, attr)
        if flags & os.O_WRONLY:
            if flags & os.O_APPEND:
                fstr = 'ab'
            else:
                fstr = 'wb'
        elif flags & os.O_RDWR:
            if flags & os.O_APPEND:
                fstr = 'a+b'
            else:
                fstr = 'r+b'
        else:
            # O_RDONLY (== 0)
            fstr = 'rb'
        try:
            f = os.fdopen(fd, fstr)
        except OSError as e:
            print(e)
            return paramiko.SFTPServer.convert_errno(e.errno)
        fobj = paramiko.StubSFTPHandle(flags)
        fobj.filename = path
        fobj.readfile = f
        fobj.writefile = f
        print("yay....")
        return fobj
