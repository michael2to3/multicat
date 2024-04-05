from pathlib import Path
from typing import List

from .search_strategy import ISearchStrategy
from .substr_search import SubstrSearch


class FileManager:
    def __init__(
        self,
        rules_dir: str,
        wordlists_dir: str,
        search_strategy: ISearchStrategy = SubstrSearch(),
    ):
        self.rules_dir = Path(rules_dir).resolve()
        self.wordlists_dir = Path(wordlists_dir).resolve()
        self.search_strategy = search_strategy
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        self.wordlists_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_path(self, base_dir: Path, path: str | Path) -> Path:
        if isinstance(path, str):
            path = Path(path)
        resolved_path = (base_dir / path).resolve()
        if base_dir not in resolved_path.parents and base_dir != resolved_path:
            raise ValueError("Attempted directory traversal detected")
        return resolved_path

    def _search_file(self, directory: Path, filename: str) -> Path:
        if self.search_strategy:
            return Path(self.search_strategy.search_for_file(str(directory), filename))
        else:
            sanitized_path = self._sanitize_path(directory, filename)
            if sanitized_path.is_file():
                return sanitized_path
            else:
                raise FileNotFoundError(f"File not found: {filename}")

    def get_rules_files(self) -> List[str]:
        return [str(file) for file in self.rules_dir.glob("*") if file.is_file()]

    def get_wordlists_files(self) -> List[str]:
        return [str(file) for file in self.wordlists_dir.glob("*") if file.is_file()]

    def exist_wordlist(self, filename: str) -> bool:
        try:
            return self._search_file(self.wordlists_dir, filename).is_file()
        except (FileNotFoundError, ValueError):
            return False

    def exist_rules(self, filename: str) -> bool:
        try:
            return self._search_file(self.rules_dir, filename).is_file()
        except (FileNotFoundError, ValueError):
            return False

    def add_rule_file(self, file_name: str, content: str):
        try:
            file_path = self._sanitize_path(self.rules_dir, file_name)
            file_path.write_text(content)
        except ValueError:
            raise ValueError("Invalid file path for rule file")

    def add_wordlist_file(self, file_name: str, content: str):
        try:
            file_path = self._sanitize_path(self.wordlists_dir, file_name)
            file_path.write_text(content)
        except ValueError:
            raise ValueError("Invalid file path for wordlist file")

    def get_wordlist(self, filename: str) -> str:
        try:
            return str(self._search_file(self.wordlists_dir, filename))
        except FileNotFoundError:
            raise FileNotFoundError(f"Wordlist file not found: {filename}")

    def get_rule(self, filename: str) -> str:
        try:
            return str(self._search_file(self.rules_dir, filename))
        except FileNotFoundError:
            raise FileNotFoundError(f"Rules file not found: {filename}")
