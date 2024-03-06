from celery import shared_task


@shared_task
def process_hash(hashes):
    print(f"Processing hashes: {hashes}")
    return "Hashes processed"
