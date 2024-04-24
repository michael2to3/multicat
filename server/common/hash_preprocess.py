from abc import ABC, abstractmethod
from typing import List


class HashPreStrategy(ABC):
    @abstractmethod
    def do(self, hashes: List[str]):
        pass


class NTLMStrategy(HashPreStrategy):
    is_nt: bool

    def __init__(self, is_nt: bool):
        self.is_nt = is_nt

    def do(self, hashes: List[str]):
        sample = hashes[0]
        sep = ":"
        if len(sample.split(sep)) != 7:
            return

        sep_idx = 3 if self.is_nt else 2
        for i, hash in enumerate(hashes):
            hashes[i] = hash.split(sep)[sep_idx]


class HashPreprocessorContext:
    _strategy: HashPreStrategy

    def __init__(self, strategy: HashPreStrategy):
        self._strategy = strategy

    def preprocess(self, hashes: List[str]):
        self._strategy.do(hashes)


hash_processor_map = {
    "1000": NTLMStrategy(is_nt=True),
    "3000": NTLMStrategy(is_nt=False),
}


class HashPreprocessor:
    def __init__(self, hashtype):
        self.hashtype = hashtype

    def preprocess(self, hashes) -> List[str]:
        strategy = hash_processor_map.get(self.hashtype)
        if strategy:
            preprocessor= HashPreprocessorContext(strategy)
            preprocessor.preprocess(hashes)
        else:
            raise NotImplemented(f"No strategy available for hashtype {self.hashtype}")

        return list(set(hashes))
