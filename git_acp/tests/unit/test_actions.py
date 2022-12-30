# import sys
# import os.path as path
# sys.path.append(path.abspath(path.join(__file__ ,"../..")))

# from unittest import TestCase
# from actions import Git

# class TestActions(TestCase):

#     def __init__(self):
#         params = {
#             "url": "test.com",
#             "path": "$PWD",
#             "git_path": "sbin/",
#             "ssh_params": None
#         }
#         my_git = Git(**params)

#     def test_set_git_ssh(self):
#         self.assertTrue(get_bin_path("git"))
#         with self.assertRaises(ValueError):
#             get_bin_path("fake")
