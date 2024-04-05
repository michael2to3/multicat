from config import Config

from .filemanager import FileManager
from .fuzzyengine import FuzzySearchEngine


class WordlistManager(FileManager):
    def __init__(self):
        super(Config.get("WORDLIST_DIR"), FuzzySearchEngine())
