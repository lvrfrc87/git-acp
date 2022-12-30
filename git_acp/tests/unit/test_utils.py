import sys
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"../..")))
import tempfile

from unittest import TestCase, main
from utils import get_bin_path, write_ssh_wrapper

class TestUtils(TestCase):

    def test_get_bin_path(self):
        self.assertTrue(get_bin_path("git"))
        with self.assertRaises(ValueError):
            get_bin_path("fake")

    def test_write_ssh_wrapper(self):
        wrapper_path, tmpdir = write_ssh_wrapper()
        self.assertTrue(wrapper_path)
        tmpdir.cleanup()

    def test_write_ssh_wrapper(self):
        pass

if __name__ == '__main__':
    main()