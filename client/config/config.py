import os
from enum import Enum


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigKey(str, Enum):
    ASSETS_DIR = "ASSETS_DIR"
    DATABASE_URL = "DATABASE_URL"
    WORKER_NAME = "WORKER_NAME"


class Config:
    @staticmethod
    def get(key: str) -> str:
        value = os.environ.get(key)
        if value is not None:
            return value
        raise ValueError(f"Environment variable {key} is not set")
