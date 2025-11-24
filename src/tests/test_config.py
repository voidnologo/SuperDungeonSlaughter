import unittest
from pathlib import Path

from src.config import DATA_DIR, MONSTERS_FILE, PROJECT_ROOT, SCORES_FILE


class ConfigTests(unittest.TestCase):
    def test_project_root_is_path_object(self):
        self.assertIsInstance(PROJECT_ROOT, Path)

    def test_project_root_exists(self):
        self.assertTrue(PROJECT_ROOT.exists())

    def test_data_dir_is_path_object(self):
        self.assertIsInstance(DATA_DIR, Path)

    def test_data_dir_is_subdirectory_of_project_root(self):
        self.assertTrue(str(DATA_DIR).startswith(str(PROJECT_ROOT)))

    def test_monsters_file_has_correct_name(self):
        self.assertEqual('monsters.json', MONSTERS_FILE.name)

    def test_monsters_file_exists(self):
        self.assertTrue(MONSTERS_FILE.exists())

    def test_scores_file_has_correct_name(self):
        self.assertEqual('scores.json', SCORES_FILE.name)

    def test_scores_file_path_in_data_dir(self):
        self.assertEqual(DATA_DIR, SCORES_FILE.parent)
