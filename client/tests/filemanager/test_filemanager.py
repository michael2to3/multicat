import unittest
from unittest.mock import Mock, patch

from filemanager import FileManager


class TestFileManager(unittest.TestCase):
    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.resolve", return_value=Mock(is_file=Mock(return_value=True)))
    def test_exists_file_found(self, mocked_resolve, mocked_mkdir):
        search_engine_mock = Mock()
        search_engine_mock.search_for_file.return_value = Mock(
            is_file=Mock(return_value=True)
        )
        fm = FileManager("/test/dir", search_engine=search_engine_mock)
        self.assertTrue(fm.exists_file("filename"))

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.resolve", return_value=Mock(is_file=Mock(return_value=False)))
    def test_exists_file_not_found(self, mocked_resolve, mocked_mkdir):
        search_engine_mock = Mock()
        search_engine_mock.search_for_file.side_effect = FileNotFoundError
        fm = FileManager("/test/dir", search_engine=search_engine_mock)
        self.assertFalse(fm.exists_file("filename"))
