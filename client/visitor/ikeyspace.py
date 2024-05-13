from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas import (
        KeyspaceCombinatorSchema,
        KeyspaceHybridSchema,
        KeyspaceMaskSchema,
        KeyspaceStraightSchema,
    )


class IKeyspaceVisitor(ABC):
    @abstractmethod
    def process_straight(self, schema: "KeyspaceStraightSchema"):
        pass

    @abstractmethod
    def process_combinator(self, schema: "KeyspaceCombinatorSchema"):
        pass

    @abstractmethod
    def process_mask(self, schema: "KeyspaceMaskSchema"):
        pass

    @abstractmethod
    def process_hybrid(self, schema: "KeyspaceHybridSchema"):
        pass
