import gzip
import io


class BackupManager:

    def __init__(self, shell):
        self._shell = shell

    def config_dir(self):
        """
        Backs up the /etc/config directory on the OpenWRT instance and returns it as a GZIP-compressed
        blob of a tar archive.
        """
        uncompressed_tar = bytes(self._shell.execute('tar -c /etc/config').encode('utf-8'))
        compressed_tar = io.BytesIO()
        gz = gzip.GzipFile(fileobj=compressed_tar, mode='wb')
        gz.write(uncompressed_tar)
        gz.close()

        compressed_tar.seek(0)
        return compressed_tar.read()