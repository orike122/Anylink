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

    def open(self, sftp_path, flags, attr):
        local_path = self._local_path(sftp_path)
        print(local_path)
        handle = paramiko.SFTPHandle()
        handle.readfile = open(local_path, "wb+")
        return handle

    def remove(self, path):
        path = self._local_path(path)
        try:
            os.remove(path)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        return paramiko.SFTP_OK


    def rename(self, oldpath, newpath):
        oldpath = self._local_path(oldpath)
        newpath = self._local_path(newpath)
        try:
            os.rename(oldpath, newpath)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        return paramiko.SFTP_OK

    def mkdir(self, path, attr):
        path = self._local_path(path)
        try:
            os.mkdir(path)
            if attr is not None:
                paramiko.SFTPServer.set_file_attr(path, attr)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        return paramiko.SFTP_OK

    def rmdir(self, path):
        path = self._local_path(path)
        try:
            os.rmdir(path)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        return paramiko.SFTP_OK

    def chattr(self, path, attr):
        path = self._local_path(path)
        try:
            paramiko.SFTPServer.set_file_attr(path, attr)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        return paramiko.SFTP_OK

    def symlink(self, target_path, path):
        path = self._local_path(path)
        if (len(target_path) > 0) and (target_path[0] == '/'):
            # absolute symlink
            target_path = os.path.join(self.ROOT, target_path[1:])
            if target_path[:2] == '//':
                # bug in os.path.join
                target_path = target_path[1:]
        else:
            # compute relative to path
            abspath = os.path.join(os.path.dirname(path), target_path)
            if abspath[:len(self.ROOT)] != self.ROOT:
                # this symlink isn't going to work anyway -- just break it immediately
                target_path = '<error>'
        try:
            os.symlink(target_path, path)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        return paramiko.SFTP_OK

    def readlink(self, path):
        path = self._local_path(path)
        try:
            symlink = os.readlink(path)
        except OSError as e:
            return paramiko.SFTPServer.convert_errno(e.errno)
        # if it's absolute, remove the root
        if os.path.isabs(symlink):
            if symlink[:len(self.ROOT)] == self.ROOT:
                symlink = symlink[len(self.ROOT):]
                if (len(symlink) == 0) or (symlink[0] != '/'):
                    symlink = '/' + symlink
            else:
                symlink = '<error>'

        return symlink
