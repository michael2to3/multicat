import logging
from pathlib import Path

from .fuzzyengine import FuzzySearchEngine
from .searchengine import BaseSearchEngine

logger = logging.getLogger(__name__)


class FileManager:
    def __init__(
        self,
        search_dir: str,
        search_engine: BaseSearchEngine = FuzzySearchEngine(),
    ):
        logger.warn(
            "Deprecated: Use 'filemanager.rulesmanager.RulesManager and 'filemanager.wordlistmanager.WordlistManager' instead"
        )

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
