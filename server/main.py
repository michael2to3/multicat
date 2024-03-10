import logging
from config import CeleryApp

app = CeleryApp("server").get_app()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.task
def get_wordlists():
    result = app.send_task("main.get_wordlists", queue="client")
    return result


@app.task
def get_rules():
    result = app.send_task("main.get_rules", queue="client")
    return result
