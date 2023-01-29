import os
import sys
import tempfile
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"../../..")))

from unittest import TestCase
from actions import Git

class TestActions(TestCase):

    def setUp(self) -> None:
        self.gitlab_token = os.environ['GITLAB_TOKEN']
        if not self.gitlab_token:
            raise Exception("GitLab token is required in env variable -> $GITLAB_TOKEN")
        

        clone = os.system(f"git -C /tmp/ clone https://Federico87:{self.gitlab_token}@gitlab.com/networkAutomation/git-acp-integration-tests.git")
        if clone != 0:
            raise Exception("Something went wrong while cloning the repo.")

        self.random_filename = tempfile.NamedTemporaryFile(dir="/tmp/git-acp-integration-tests")

    def tearDown(self) -> None:
        os.system("rm -rf /tmp/git-acp-integration-tests")

    def test_git_add(self):
        params = {
            "url": "https://gitlab.com/networkAutomation/git-acp-integration-tests.git",
            "path": "/tmp/",
            "git_path": "sbin/",
            "add": self.random_filename.name
        }
        my_git = Git(**params)
        breakpoint()
        result = my_git.add()

