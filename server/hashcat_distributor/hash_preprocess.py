from abc import ABC, abstractmethod


class HashPreStrategy(ABC):
    @abstractmethod
    def do(self, hashes: list[str]) -> list[str]:
        pass


class NTLMStrategy(HashPreStrategy):
    is_nt: bool

    def __init__(self, is_nt: bool):
        self.is_nt = is_nt

    def do(self, hashes: list[str]) -> list[str]:
        sep = ":"
        result = []

        sep_idx = 3 if self.is_nt else 2
        for hash in hashes:
            if len(hash.split(sep)) != 7:
                result.append(hash)
            else:
                result.append(hash.split(sep)[sep_idx])

        return result


class DummyStrategy(HashPreStrategy):
    def do(self, hashes: list[str]) -> list[str]:
        return hashes.copy()


class HashPreprocessorContext:
    _strategy: HashPreStrategy

    def __init__(self, strategy: HashPreStrategy):
        self._strategy = strategy

    def preprocess(self, hashes: list[str]) -> list[str]:
        return self._strategy.do(hashes)


hash_processor_map = {
    "1000": NTLMStrategy(is_nt=True),
    "3000": NTLMStrategy(is_nt=False),
}


class HashPreprocessor:
    def __init__(self, hashtype):
        self.hashtype = hashtype

    def preprocess(self, hashes) -> list[str]:
        strategy = hash_processor_map.get(self.hashtype, DummyStrategy())
        preprocessor = HashPreprocessorContext(strategy)
        result = preprocessor.preprocess(hashes)

        return list(set(result))
