from typing import TYPE_CHECKING

from filemanager import FileManager
from hashcat.hashcat import HashcatInterface

if TYPE_CHECKING:
    from schemas import (
        KeyspaceCombinatorSchema,
        KeyspaceHybridSchema,
        KeyspaceMaskSchema,
        KeyspaceStraightSchema,
    )

from .ikeyspace import IKeyspaceVisitor


class KeyspaceHashcatConfigurerVisitor(IKeyspaceVisitor):
    _hashcat: HashcatInterface
    _file_manager: FileManager

    def __init__(self, hashcat: HashcatInterface, file_manager: FileManager):
        self._hashcat = hashcat
        self._fm = file_manager

    def process_straight(self, schema: "KeyspaceStraightSchema"):
        self._hashcat.dict1 = self._fm.get_file(schema.wordlist1)

        if schema.rule:
            # It's better to provide one rule at a time, because we can quickly exceed available memory, or reach integer overflow
            self._hashcat.rules = (self._fm.get_file(schema.rule),)

    def process_combinator(self, schema: "KeyspaceCombinatorSchema"):
        self._hashcat.dict1 = self._fm.get_file(schema.wordlist1)
        self._hashcat.dict2 = self._fm.get_file(schema.wordlist2)

        if schema.left:
            self._hashcat.rule_buf_l = self._fm.get_file(schema.left)

        if schema.right:
            self._hashcat.rule_buf_r = self._fm.get_file(schema.right)

    def process_mask(self, schema: "KeyspaceMaskSchema"):
        self._hashcat.mask = schema.mask

        for charset in schema.custom_charsets:
            setattr(
                self._hashcat,
                f"custom_charset_{charset.charset_id}",
                charset.charset,
            )

    def process_hybrid(self, schema: "KeyspaceHybridSchema"):
        self._hashcat.dict1 = self._fm.get_file(schema.wordlist1)
        self._hashcat.mask = schema.mask
