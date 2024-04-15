from config.config import Config, ConfigKey
from filemanager.filemanager import FileManager
from filemanager.fuzzyengine import FuzzySearchEngine


class AssetsFileManager(FileManager):
    def __init__(self):
        super().__init__(Config.get(ConfigKey.ASSETS_DIR), FuzzySearchEngine())
