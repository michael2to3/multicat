import itertools
from typing import Callable, List, TYPE_CHECKING

from schemas.keyspaces import (
    KeyspaceCombinatorSchema,
    KeyspaceHybridSchema,
    KeyspaceMaskSchema,
    KeyspaceStraightSchema,
)

if TYPE_CHECKING:
    from schemas import CombinatorStep, HybridStep, MaskStep, StraightStep

from .ihashcatstep import IHashcatStepVisitor


class HashcatStepKeyspaceVisitor(IHashcatStepVisitor):
    _callback: Callable[[List], None]

    def __init__(self, callback: Callable[[List], None]):
        self._callback = callback

    def process_straight(self, schema: "StraightStep"):
        tasks = []
        rules = schema.rules or ("",)
        for wordlist, rule in itertools.product(schema.wordlists, rules):
            tasks.append(KeyspaceStraightSchema(wordlist1=wordlist, rule=rule, value=0))
        self._callback(tasks)

    def process_combinator(self, schema: "CombinatorStep"):
        tasks = []
        left_rules = schema.left_rules or ("",)
        right_rules = schema.right_rules or ("",)

        for wordlist1, wordlist2, left, right in itertools.product(
            schema.left_wordlists, schema.right_wordlists, left_rules, right_rules
        ):
            tasks.append(
                KeyspaceCombinatorSchema(
                    wordlist1=wordlist1,
                    wordlist2=wordlist2,
                    left=left,
                    right=right,
                    value=0,
                )
            )
        self._callback(tasks)

    def process_mask(self, schema: "MaskStep"):
        tasks = []

        for mask in schema.masks:
            tasks.append(
                KeyspaceMaskSchema(
                    mask=mask, custom_charsets=schema.custom_charsets, value=0
                )
            )
        self._callback(tasks)

    def process_hybrid(self, schema: "HybridStep"):
        tasks = []

        for wordlist, mask in itertools.product(schema.wordlists, schema.masks):
            tasks.append(
                KeyspaceHybridSchema(
                    attack_mode=schema.attack_mode,
                    wordlist1=wordlist,
                    mask=mask,
                    wordlist_mask=schema.wordlist_mask,
                    custom_charsets=schema.custom_charsets,
                    value=0,
                )
            )

        self._callback(tasks)
