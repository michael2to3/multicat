from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    assets_dir: str = Field(alias="ASSETS_DIR")
    database_url: str = Field(alias="DATABASE_URL")
    worker_name: str = Field(alias="WORKER_NAME")
    celery_broker_url: str = Field(alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(alias="CELERY_RESULT_BACKEND")
    timezone: str = Field(alias="TIMEZONE")
    logger_level: str = Field(alias="LOGGER_LEVEL")
