import os
import pytest
from hashcat import FileManager
from pathlib import Path
import shutil


@pytest.fixture
def setup_file_manager(tmp_path):
    rules_dir = tmp_path / "rules"
    wordlists_dir = tmp_path / "wordlists"
    fm = FileManager(str(rules_dir), str(wordlists_dir))
    return fm, rules_dir, wordlists_dir


def test_init(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    assert rules_dir.exists()
    assert wordlists_dir.exists()


def test_add_rule_file(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    fm.add_rule_file("test_rule.txt", "dummy content")
    assert (rules_dir / "test_rule.txt").read_text() == "dummy content"


def test_add_wordlist_file(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    fm.add_wordlist_file("test_wordlist.txt", "dummy content")
    assert (wordlists_dir / "test_wordlist.txt").read_text() == "dummy content"


def test_get_rules_files(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    fm.add_rule_file("test_rule.txt", "dummy content")
    assert str(rules_dir / "test_rule.txt") in fm.get_rules_files()


def test_get_wordlists_files(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    fm.add_wordlist_file("test_wordlist.txt", "dummy content")
    assert str(wordlists_dir / "test_wordlist.txt") in fm.get_wordlists_files()


def test_exist_wordlist(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    fm.add_wordlist_file("existing_file.txt", "content")
    assert fm.exist_wordlist("existing_file.txt")
    assert not fm.exist_wordlist("non_existing_file.txt")


def test_exist_rules(setup_file_manager):
    fm, rules_dir, wordlists_dir = setup_file_manager
    fm.add_rule_file("existing_file.txt", "content")
    assert fm.exist_rules("existing_file.txt")
    assert not fm.exist_rules("non_existing_file.txt")
