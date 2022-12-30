import sys
import os.path as path
sys.path.append(path.abspath(path.join(__file__ ,"../..")))

from unittest import TestCase
from utils import get_bin_path

class TestUtils(TestCase):

    def test_get_bin_path(self):
        self.assertTrue(get_bin_path("git"))
        with self.assertRaises(ValueError):
            get_bin_path("fake")
