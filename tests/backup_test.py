import io
from fixtures import *
import tarfile
import gzip


def test_backing_up_config_dir():
    compressed_tar_blob = manager.backup.config_dir()

    tar = tarfile.open(fileobj=io.BytesIO(compressed_tar_blob), mode='r:*')
    # The configuration directory has 9 files in it, plus the config directory
    assert len(tar.getmembers()) == 9+1
