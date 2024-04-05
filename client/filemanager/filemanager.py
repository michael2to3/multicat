from pathlib import Path

from .fuzzyengine import FuzzySearchEngine
from .searchengine import BaseSearchEngine


class FileManager:
    def __init__(
        self,
        search_dir: str,
        search_engine: BaseSearchEngine = FuzzySearchEngine(),
    ):
        self._search_dir = Path(search_dir).resolve()
        self._search_engine = search_engine

        self._search_dir.mkdir(parents=True, exist_ok=True)

    def exists_file(self, filename: str) -> bool:
        try:
            return self._search_engine.search_for_file(
                self._search_dir, filename
            ).is_file()
        except (FileNotFoundError, ValueError):
            return False

    def get_file(self, filename: str) -> str:
        return str(self._search_engine.search_for_file(self._search_dir, filename))
