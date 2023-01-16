import sys
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"../..")))

from unittest import TestCase
from actions import Git

class TestActions(TestCase):


    def test_git_add(self):
        params = {
            "url": "test.com",
            "path": "/tmp/",
            "git_path": "sbin/",
        }
        my_git = Git(**params)

        result = my_git.add()
