import base64
import io
from typing import List

from celery import current_app, shared_task

import gnupg
from config import Database
from schemas import CeleryResponse, HashcatStep

db = Database()


def generate_discrete_task(namerule: str, hashtype: str, hashes: List[str]):
    steps: List[HashcatStep]


@shared_task(name="main.run_hashcat")
def run_hashcat(hashtype, namerule, base64_encrypt_hashes):
    gpg = gnupg.GPG()

    encrypt_hashes = base64.b64decode(base64_encrypt_hashes)
    hashes_in_memory = io.BytesIO(encrypt_hashes)

    decrypted_data = gpg.decrypt_file(hashes_in_memory)

    if not decrypted_data.ok:
        return CeleryResponse(error="Failed to decrypt the file").dict()

    hashes = decrypted_data.data

    result = current_app.send_task("main.run_hashcat", args=(hashes,), queue="server")
    job_id = result.get(timeout=60)

    message = f"Your task has been queued and will start as soon as a server becomes available. You can check the progress of your task using the command /status {job_id}. Thank you for your patience."

    return CeleryResponse(value=message).dict()
