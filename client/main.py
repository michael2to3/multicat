import os
import logging
import asyncio
from .model import Request
from .hashcat import HashcatManager, HashcatException, FileManager
from .config import CeleryApp, Config

app = CeleryApp("client").get_app()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))


@app.task(bind=True)
def run_hashcat(self, request: dict):
    request_model = Request(**request)
    manager = HashcatManager(file_manager)

    manager.add_option("-m", request_model.mode.value)

    if request_model.wordlists:
        for wordlist in request_model.wordlists:
            manager.add_option(wordlist)

    if request_model.masks:
        for mask in request_model.masks:
            manager.add_option(mask)

    if request_model.rules_files:
        for rules_file in request_model.rules_files:
            manager.add_option("-r", rules_file)

    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(manager.run())
        return result
    except HashcatException as e:
        self.update_state(
            state="FAILURE", meta={"exc_type": type(e).__name__, "exc_message": str(e)}
        )
        raise e
