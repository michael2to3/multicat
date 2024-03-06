from celery import Celery

app = Celery("server")
app.config_from_object("celeryconfig")


@app.task
def process_hashes(hashes):
    print(f"Processing hashes: {hashes}")
    return "Hashes processed"
