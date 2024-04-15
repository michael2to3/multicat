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
        fse = FuzzySearchEngine(0.6)
        with self.assertRaises(FileNotFoundError):
            fse.search_for_file(Path("/test/dir"), "nonexistent")

    @patch("pathlib.Path.rglob")
    def test_search_with_path_traversal_attempts(self, mocked_rglob):
        mocked_rglob.return_value = [Path("/test/dir/safe_file.txt")]
        fse = FuzzySearchEngine(0.0)

        traversal_attempts = [
            "../",
            "a/../b/../etc/passwd",
            "/tmp////etc/passwd",
            "../../../etc/passwd",
            "./././../etc/passwd",
        ]

        for attempt in traversal_attempts:
            with self.subTest(attempt=attempt):
                result = fse.search_for_file(Path("/test/dir"), attempt)
                self.assertTrue(
                    "/test/dir" in str(result),
                    f"Path traversal attempt was not neutralized for {attempt}",
                )
