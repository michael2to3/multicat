import subprocess
import logging
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, app, client_id):
        self.app = app
        self.client_id = client_id
        self.hashcat_process = None

    def __enter__(self):
        self.register_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unregister_client()

    def register_client(self):
        self.app.send_task("register_client", args=[self.client_id])
        logger.info(f"Client {self.client_id} registered")

    def unregister_client(self):
        self.app.send_task("unregister_client", args=[self.client_id])
        logger.info(f"Client {self.client_id} unregistered")

    def start_hashcat(self, hash_file, wordlist):
        hashcat_cmd = f"hashcat -m 0 {hash_file} {wordlist}"
        self.hashcat_process = subprocess.Popen(
            hashcat_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logger.info("Hashcat process started")

    def stop_hashcat(self):
        if self.hashcat_process:
            self.hashcat_process.terminate()
            logger.info("Hashcat process stopped")

    def get_gpu_metrics(self):
        gpu_usage = psutil.sensors_temperatures().get("gpu", [])
        return gpu_usage
