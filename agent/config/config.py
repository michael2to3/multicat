from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    celery_broker_url: str = Field(alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(alias="CELERY_RESULT_BACKEND")
    timezone: str = Field(alias="TIMEZONE")
    telegram_token: str = Field(alias="TELEGRAM_TOKEN")
    logger_level: str = Field(alias="LOGGER_LEVEL")
