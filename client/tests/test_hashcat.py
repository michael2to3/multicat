import pytest
from unittest.mock import MagicMock

from schemas import HashcatOption
from hashcat import HashcatException, HashcatManager, FileManager


@pytest.fixture
def hashcat_manager():
    file_manager_mock = MagicMock(FileManager)
    return HashcatManager("hashcat", file_manager_mock)


def test_add_option_rules_file_not_found(hashcat_manager):
    hashcat_manager.file_manager.exist_rules.return_value = False

    with pytest.raises(FileNotFoundError) as e:
        hashcat_manager.add_option(HashcatOption.RULES_FILE, "nonexistent_rules.txt")
    assert str(e.value) == "Rules file not found: nonexistent_rules.txt"


def test_add_option_wordlist_file_not_found(hashcat_manager):
    hashcat_manager.file_manager.exist_wordlist.return_value = False

    with pytest.raises(FileNotFoundError) as e:
        hashcat_manager.add_option(
            HashcatOption.WORDLIST_FILE, "nonexistent_wordlist.txt"
        )
    assert str(e.value) == "Wordlist file not found: nonexistent_wordlist.txt"


def test_add_option_invalid_value_type(hashcat_manager):
    with pytest.raises(HashcatException) as e:
        hashcat_manager.add_option(HashcatOption.RULES_FILE, 123)
    assert str(e.value) == "Rules file must be a string: 123"


def test_run_success(hashcat_manager):
    hashcat_manager.file_manager.exist_rules.return_value = True
    hashcat_manager.file_manager.exist_wordlist.return_value = True
    hashcat_manager.run = MagicMock(return_value="hashcat execution success")

    result = hashcat_manager.run()
    assert result == "hashcat execution success"


def test_run_failure(hashcat_manager):
    hashcat_manager.file_manager.exist_rules.return_value = True
    hashcat_manager.file_manager.exist_wordlist.return_value = True
    hashcat_manager.run = MagicMock(
        side_effect=HashcatException("Hashcat error: something went wrong")
    )

    with pytest.raises(HashcatException) as e:
        hashcat_manager.run()
    assert str(e.value) == "Hashcat error: something went wrong"
