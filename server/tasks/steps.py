from pydantic import ValidationError, parse_obj_as
import yaml
from celery import shared_task
from schemas import hashcat_step_constructor, Steps


@shared_task(name="main.liststeps")
def liststeps():
    return "Started..."

@shared_task(name="main.loadsteps")
def loadsteps(rule):
    yaml.SafeLoader.add_constructor("!hashcatstep", hashcat_step_constructor)
    try:
        data = yaml.safe_load(rule)
        model = parse_obj_as(Steps, data)
    except yaml.YAMLError as ye:
        return f"Failed to load YAML content: {str(ye)}"
    except ValidationError as ve:
        return f"Validation error for the provided data: {str(ve)}"

    task_data = model.json()

    #result = current_app.send_task( "main.run_hashcat", args=(task_data,), queue="server")

    return task_data
