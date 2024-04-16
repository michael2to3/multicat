from pydantic import AmqpDsn, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    assets_dir: str = Field(alias="ASSETS_DIR")
    database_url: PostgresDsn = Field(alias="DATABASE_URL")
    worker_name: str = Field(alias="WORKER_NAME")
    celery_broker_url: AmqpDsn = Field(alias="CELERY_BROKER_URL")
    celery_result_backend: RedisDsn = Field(alias="CELERY_RESULT_BACKEND")
    timezone: str = Field(alias="TIMEZONE")
    hashcat_type_gpu: str = Field(alias="HASHCAT_TYPE_GPU")
    hc_path: str = Field(alias="HC_PATH")
    telegram_token: str = Field(alias="TELEGRAM_TOKEN")
