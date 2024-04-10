import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config:
    @staticmethod
    def get(key: str) -> str:
        value = os.environ.get(key)
        if value is not None:
            return value
        raise ValueError(f"Environment variable {key} is not set")
