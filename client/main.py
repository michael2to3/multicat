import subprocess
import logging
from celery import Celery
import psutil
import celeryconfig
from client import Client
from time import sleep

app = Celery("client")
app.config_from_object(celeryconfig)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    client_id = "client_001"
    hash_file = "path/to/hashfile"
    wordlist = "path/to/wordlist"

    with Client(client_id) as client:
        client.start_hashcat(hash_file, wordlist)
        while client.hashcat_process.poll() is None:
            gpu_metrics = client.get_gpu_metrics()
            logger.info(f"GPU Metrics: {gpu_metrics}")
            sleep(1)

        client.stop_hashcat()
