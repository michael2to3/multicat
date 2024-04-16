from celery import Celery
from kombu import Exchange, Queue
from kombu.common import Broadcast

from .config import Config


class CeleryApp:
    def __init__(self, name):
        self.app = Celery(name)
        self.configure_celery()

    def configure_celery(self):
        broadcast_exchange = Exchange("broadcast_exchange", type="fanout")
        default_exchange = Exchange("default", type="direct")

        self.app.conf.task_queues = (
            Queue("client", exchange=default_exchange, routing_key="client.#"),
            Broadcast("broadcast", exchange=broadcast_exchange),
        )

        self.app.conf.task_default_queue = "client"
        self.app.conf.task_default_exchange = "default"
        self.app.conf.task_routes = {
            "b.*": {"queue": "broadcast"},
            "client.*": {"queue": "client"},
        }

        self.app.conf.update(
            broker_url=Config().celery_broker_url,
            result_backend=Config().celery_broker_url,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone=Config().timezone,
            enable_utc=True,
        )

    def get_app(self):
        return self.app
