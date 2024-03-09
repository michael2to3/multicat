import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from typing import Optional, Union

from model import HashcatOption
from hashcat import HashcatException, HashcatManager, FileManager


class TestHashcatManager(unittest.TestCase):

    def setUp(self) -> None:
        self.file_manager_mock = FileManager(".", ".")
        self.hashcat_manager = HashcatManager("hashcat", self.file_manager_mock)

    def test_add_option_rules_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as context:
            self.hashcat_manager.add_option(
                HashcatOption.RULES_FILE, "nonexistent_rules.txt"
            )
        self.assertEqual(
            str(context.exception), "Rules file not found: nonexistent_rules.txt"
        )

    def test_add_option_wordlist_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as context:
            self.hashcat_manager.add_option(
                HashcatOption.WORDLIST_FILE, "nonexistent_wordlist.txt"
            )
        self.assertEqual(
            str(context.exception), "Wordlist file not found: nonexistent_wordlist.txt"
        )

    def test_add_option_invalid_value_type(self):
        with self.assertRaises(HashcatException) as context:
            self.hashcat_manager.add_option(HashcatOption.RULES_FILE, 123)
        self.assertEqual(str(context.exception), "Rules file must be a string: 123")

    def test_run_success(self):
        self.hashcat_manager.run = AsyncMock(return_value="hashcat execution success")
        result = asyncio.run(self.hashcat_manager.run())
        self.assertEqual(result, "hashcat execution success")

    def test_run_failure(self):
        self.hashcat_manager.run = AsyncMock(
            side_effect=HashcatException("Hashcat error: something went wrong")
        )
        with self.assertRaises(HashcatException) as context:
            asyncio.run(self.hashcat_manager.run())
        self.assertEqual(str(context.exception), "Hashcat error: something went wrong")
