from pathlib import Path
from typing import List

from .search_strategy import ISearchStrategy


class SubstrSearch(ISearchStrategy):
    def __init__(self, search_dirs: List[Path]):
        self.search_dirs = search_dirs

    def search_for_file(self, search_term: str) -> str:
        for directory in self.search_dirs:
            direct_match = directory / search_term
            if direct_match.is_file():
                return str(direct_match)

        for directory in self.search_dirs:
            for file in directory.glob("*"):
                if search_term in file.name:
                    return str(file)
        raise FileNotFoundError(f"No file found containing: {search_term}")
