import gnupg
from celery import shared_task

@shared_task(name="main.get_pubkey")
def get_pubkey():
    gpg = gnupg.GPG()
    key_identifier = "muclicat@deiteriy.com"
    public_keys = gpg.export_keys(key_identifier)
    return public_keys.encode("utf-8")
