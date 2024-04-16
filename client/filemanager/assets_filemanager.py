from config.config import Config
from filemanager.filemanager import FileManager
from filemanager.fuzzyengine import FuzzySearchEngine


class AssetsFileManager(FileManager):
    def __init__(self):
        super().__init__(Config.assets_dir, FuzzySearchEngine(0.6))
