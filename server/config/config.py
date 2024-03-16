import os


class Config:
    @staticmethod
    def get(key: str):
        if os.environ.get(key):
            return os.environ.get(key)
        raise ValueError(f"Environment variable {key} is not set")
