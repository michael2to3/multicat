from abc import ABC, abstractmethod


class ISearchStrategy(ABC):
    @abstractmethod
    def search_for_file(self, search_term: str) -> str:
        pass
