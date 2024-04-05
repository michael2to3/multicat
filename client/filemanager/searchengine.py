from abc import ABC, abstractmethod
from pathlib import Path


class BaseSearchEngine(ABC):
    @abstractmethod
    async def _search_for_file(self, base_dir: Path, search_term: str) -> Path:
        pass

    async def search_for_file(self, base_dir: Path, search_term: str) -> Path:
        rpath = self._sanitize_path(base_dir, Path(search_term))
        if rpath.is_file():
            return rpath

        return self._search_for_file(base_dir, search_term)

    def _sanitize_path(self, base_dir: Path, path: Path) -> Path:
        resolved_path = (base_dir / path).resolve()
        if base_dir not in resolved_path.parents and base_dir != resolved_path:
            raise ValueError("Attempted directory traversal detected")
        return resolved_path
