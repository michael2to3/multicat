import io

import yaml
from celery import current_app, shared_task
from pydantic import ValidationError, parse_obj_as

import gnupg
from schemas import CeleryResponse, Steps, hashcat_step_constructor


def generate_discrete_task(rule, hashes):
    pass


@shared_task(name="main.hashcat_run")
def hashcat_run(hashtype, namerule, hashes):
    gpg = gnupg.GPG()

    hashes_in_memory = io.BytesIO(hashes)

    decrypted_data = gpg.decrypt_file(hashes_in_memory)

    if not decrypted_data.ok:
        return CeleryResponse(error="Failed to decrypt the file").dict()

    try:
        yaml.SafeLoader.add_constructor("!hashcatstep", hashcat_step_constructor)
        data = yaml.safe_load(decrypted_data.data)
        model = parse_obj_as(Steps, {"steps": data})
    except yaml.YAMLError as ye:
        return CeleryResponse(error=f"Failed to load YAML content: {str(ye)}").dict()
    except ValidationError as ve:
        return CeleryResponse(
            error=f"Validation error for the provided data: {str(ve)}"
        ).dict()

    task_data = model.json()

    result = current_app.send_task(
        "main.run_hashcat", args=(task_data,), queue="server"
    )
    result.forget()

    return CeleryResponse(value="Started...").dict()
