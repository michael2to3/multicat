from celery import Celery
import celeryconfig
from celery.schedules import crontab
from datetime import datetime, timedelta
import logging

app = Celery("server")
app.config_from_object(celeryconfig)
app.autodiscover_tasks(["tasks"], force=True)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.task
def send_to_client():
    pass
