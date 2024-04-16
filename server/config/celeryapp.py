from celery import Celery

from .config import Config


class CeleryApp:
    def __init__(self, name):
        self.app = Celery(name)
        self.configure_celery()

    def configure_celery(self):
        self.app.conf.update(
            broker_url=Config.celery_broker_url,
            result_backend=Config.celery_result_backend,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone=Config.timezone,
            enable_utc=True,
            task_routes={
                "b.*": {
                    "queue": "broadcast",
                    "exchange": "broadcast_exchange",
                    "routing_key": "broadcast",
                },
                "client.*": {"queue": "client"},
            },
        )

    def get_app(self):
        return self.app
