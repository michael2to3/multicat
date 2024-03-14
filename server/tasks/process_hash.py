import gnupg
from pydantic import BaseModel, Field, validator, ValidationError, parse_obj_as
from typing import List, Union
import yaml
from celery import current_app, shared_task
from schemas import hashcat_step_constructor, Steps


@shared_task(name="main.process_hash")
def process_hash(options, hashes):
    gpg = gnupg.GPG()
    decrypted_data = gpg.decrypt_file(hashes)

    if not decrypted_data.ok:
        return "Failed to decrypt the file"

    yaml.SafeLoader.add_constructor("!hashcatstep", hashcat_step_constructor)
    data = yaml.safe_load(decrypted_data.data)

    try:
        data = yaml.safe_load(decrypted_data.data)
        model = parse_obj_as(Steps, {"steps": data})
    except yaml.YAMLError as ye:
        return f"Failed to load YAML content: {str(ye)}"
    except ValidationError as ve:
        return f"Validation error for the provided data: {str(ve)}"

    task_data = model.json()

    result = current_app.send_task(
        "main.run_hashcat", args=(task_data,), queue="server"
    )
    return "Started..."
