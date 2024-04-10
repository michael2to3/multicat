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
    def configure_straight(self, schema: "KeyspaceStraightSchema"):
        pass

    @abstractmethod
    def configure_combinator(self, schema: "KeyspaceCombinatorSchema"):
        pass

    @abstractmethod
    def configure_mask(self, schema: "KeyspaceMaskSchema"):
        pass

    @abstractmethod
    def configure_hybrid(self, schema: "KeyspaceHybridSchema"):
        pass
