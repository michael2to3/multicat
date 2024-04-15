from config import Config

from .filemanager import FileManager
from .fuzzyengine import FuzzySearchEngine


class RulesManager(FileManager):
    def __init__(self):
        super(Config.get("RULES_DIR"), FuzzySearchEngine())
