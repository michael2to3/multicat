from celery import Celery
import celeryconfig

app = Celery("server")
app.config_from_object(celeryconfig)
app.autodiscover_tasks(["tasks"], force=True)
