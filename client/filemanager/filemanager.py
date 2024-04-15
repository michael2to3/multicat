from pathlib import Path

from .searchengine import BaseSearchEngine


class FileManager:
    def __init__(
        self,
        search_dir: str,
        search_engine: BaseSearchEngine,
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

    def get_all_files(self) -> list[str]:
        return [
            str(file_path)
            for file_path in self._search_dir.rglob("*")
            if file_path.is_file()
        ]
