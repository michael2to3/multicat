import os
import asyncio
from typing import Optional, Union
from schemas import HashcatOption
from .filemanager import FileManager


class HashcatException(Exception):
    pass


class HashcatManager:
    lock_file = "/tmp/hashcat_manager.lock"

    def __init__(self, hashcat_path: str, file_manager: FileManager):
        self.hashcat_path = hashcat_path
        self.cmd = [self.hashcat_path]
        self.file_manager = file_manager

    def add_option(
        self, option: HashcatOption, value: Optional[Union[str, int]] = None
    ):
        self.validation(option, value)

        self.cmd.append(option.value)
        if value is not None:
            self.cmd.append(str(value))

    def validation(self, option: HashcatOption, value: Optional[Union[str, int]]):
        if option == HashcatOption.RULES_FILE:
            if isinstance(value, int) or value is None:
                raise HashcatException(f"Rules file must be a string: {value}")
            if not self.file_manager.exist_rules(value):
                raise FileNotFoundError(f"Rules file not found: {value}")
        elif option == HashcatOption.WORDLIST_FILE and value:
            if isinstance(value, int) or value is None:
                raise HashcatException(f"Wordlist file must be a string: {value}")
            if not self.file_manager.exist_wordlist(value):
                raise FileNotFoundError(f"Wordlist file not found: {value}")

    async def run(self):
        if os.path.exists(self.lock_file):
            raise HashcatException(f"Hashcat is already running: {self.lock_file}")
        try:
            open(self.lock_file, "w").close()

            process = await asyncio.create_subprocess_exec(
                *self.cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                raise HashcatException(f"Hashcat error: {stderr.decode().strip()}")
            return stdout.decode().strip()
        finally:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
