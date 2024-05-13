from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas import (
        StraightStep,
        CombinatorStep,
        MaskStep,
        HybridStep,
    )


class IHashcatStepVisitor(ABC):
    @abstractmethod
    def process_straight(self, schema: "StraightStep"):
        pass

    @abstractmethod
    def process_combinator(self, schema: "CombinatorStep"):
        pass

    @abstractmethod
    def process_mask(self, schema: "MaskStep"):
        pass

    @abstractmethod
    def process_hybrid(self, schema: "HybridStep"):
        pass
