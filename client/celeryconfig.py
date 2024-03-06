import os

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = os.environ.get("CELERY_TIMEZONE", "Europe/Moscow")
enable_utc = True
