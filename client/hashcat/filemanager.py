import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class FileManager:
    def __init__(self, rules_dir: str, wordlists_dir: str):
        logger.warn("DeprecationWarning: Use the 'filemanager.filemanager' module instead.")

        self.rules_dir = Path(rules_dir)
        self.wordlists_dir = Path(wordlists_dir)
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        self.wordlists_dir.mkdir(parents=True, exist_ok=True)

    def get_rules_files(self) -> List[str]:
        return [str(file) for file in self.rules_dir.glob("*") if file.is_file()]

    def get_wordlists_files(self) -> List[str]:
        return [str(file) for file in self.wordlists_dir.glob("*") if file.is_file()]

    def exist_wordlist(self, filename: str) -> bool:
        return Path(self.wordlists_dir / filename).is_file()

    def exist_rules(self, filename: str) -> bool:
        return Path(self.rules_dir / filename).is_file()

    def add_rule_file(self, file_name: str, content: str):
        file_path = self.rules_dir / file_name
        file_path.write_text(content)

    def add_wordlist_file(self, file_name: str, content: str):
        file_path = self.wordlists_dir / file_name
        file_path.write_text(content)

    def get_wordlist(self, filename: str) -> str:
        if not self.exist_wordlist(filename):
            raise FileNotFoundError(f"Wordlist file not found: {filename}")
        return str(self.wordlists_dir / filename)

    def get_rule(self, filename: str) -> str:
        if not self.exist_rules(filename):
            raise FileNotFoundError(f"Rules file not found: {filename}")
        return str(self.rules_dir / filename)
