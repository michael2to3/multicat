import os


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config:
    @staticmethod
    def get(key: str):
        if os.environ.get(key):
            return os.environ.get(key)
        raise ValueError(f"Environment variable {key} is not set")
