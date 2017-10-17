from os.path import abspath, dirname, join
import unittest

from utils import data_file_path


class UtilsTest(unittest.TestCase):

    def test_data_file_path_returns_requested_file_path(self):
        fpath = data_file_path('monsters.json')
        expected = abspath(join(dirname(__file__), '..', '..', 'data', 'monsters.json'))
        self.assertEqual(fpath, expected)
