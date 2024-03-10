from celery import Celery
from .config import Config


class CeleryApp:
    def __init__(self, name):
        self.app = Celery(name)
        self.configure_celery()

    def configure_celery(self):
        self.app.conf.update(
            broker_url=Config.get("CELERY_BROKER_URL"),
            result_backend=Config.get("CELERY_RESULT_BACKEND"),
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone=Config.get("TIMEZONE"),
            enable_utc=True,
        )

    def get_app(self):
        return self.app
