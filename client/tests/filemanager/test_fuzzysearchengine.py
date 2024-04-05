import unittest
from pathlib import Path
from unittest.mock import patch

from filemanager import FuzzySearchEngine


class TestFuzzySearchEngine(unittest.TestCase):
    @patch("pathlib.Path.rglob")
    def test_search_for_file_found(self, mocked_rglob):
        mocked_rglob.return_value = [Path("/test/dir/matching_file.txt")]
        fse = FuzzySearchEngine(0.2)
        result = fse.search_for_file(Path("/test/dir"), "matching")
        self.assertEqual(str(result), "/test/dir/matching_file.txt")

    @patch("pathlib.Path.rglob")
    def test_search_for_file_not_found(self, mocked_rglob):
        mocked_rglob.return_value = []
        fse = FuzzySearchEngine()
        with self.assertRaises(FileNotFoundError):
            fse.search_for_file(Path("/test/dir"), "nonexistent")
