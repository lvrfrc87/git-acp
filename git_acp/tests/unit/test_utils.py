import os
import sys
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"../..")))
import tempfile

from unittest import TestCase, main
from utils import get_bin_path, write_ssh_wrapper, set_git_ssh

class TestUtils(TestCase):

    def test_get_bin_path(self):
        self.assertTrue(get_bin_path("git"))
        with self.assertRaises(ValueError):
            get_bin_path("fake")

    def test_write_ssh_wrapper(self):
        wrapper_path, tmpdir = write_ssh_wrapper()
        self.assertTrue(wrapper_path)
        tmpdir.cleanup()

    def test_set_git_ssh(self):
        os.environ["GIT_SSH"] = "/home/"
        set_git_ssh("/tmp/", None, None)
        self.assertEqual(os.environ["GIT_SSH"], "/tmp/")

        os.environ["GIT_KEY"] = "./ssh"
        set_git_ssh("/tmp/", "./id.rsa", None)
        self.assertEqual(os.environ["GIT_KEY"], "./id.rsa")

        set_git_ssh("/tmp/", "./id.rsa", "--force")
        self.assertEqual(os.environ["GIT_SSH_OPTS"], "--force")


if __name__ == '__main__':
    main()