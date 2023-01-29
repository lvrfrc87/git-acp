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

        self.random_filename = tempfile.NamedTemporaryFile(dir="/tmp/git-acp-integration-tests", suffix=".txt", delete=False).name.split("/")[-1]
        
        self.params = {
            "url": "https://gitlab.com/networkAutomation/git-acp-integration-tests.git",
            "path": "/tmp/git-acp-integration-tests/",
            "git_path": "sbin/",
            "add": self.random_filename,
            "comment": f"Add file: {self.random_filename}",
            "mode": "https",
            "branch": "main",
            "remote": "origin",
            "user": "Federico87",
            "token": self.gitlab_token
        }

    def tearDown(self) -> None:
        os.system("rm -rf /tmp/git-acp-integration-tests")

    def test_git_add(self):
        my_git = Git(**self.params)
        result = my_git.add()
        self.assertIsNone(result)

    def test_git_status(self):
        my_git = Git(**self.params)
        my_git.add()
        result = my_git.status()
        self.assertIn(self.random_filename, result)

    def test_git_commit(self):
        my_git = Git(**self.params)
        my_git.add()
        my_git.status()
        result = my_git.commit()
        self.assertIn(f"Add file: {self.random_filename}\n 1 file changed", result["git_commit"])
        self.assertTrue(result["changed"])

    def test_push_same_url_same_origin(self):
        pass