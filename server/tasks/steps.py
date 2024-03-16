import logging
import yaml
import json
from pydantic import BaseModel, Field, ValidationError, parse_obj_as
from celery import shared_task
from sqlalchemy.exc import SQLAlchemyError
from models import StepsModel
from config import Database, UUIDGenerator
from schemas import Steps, hashcat_step_loader, CeleryResponse

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="main.delsteps")
def delsteps(owner_id: str, namerule: str):
    try:
        uid = UUIDGenerator.generate(owner_id)
    except ValueError as ve:
        logger.error(f"Invalid UUID format: {str(ve)}")
        return CeleryResponse(error=f"Invalid UUID format: {str(ve)}").dict()

    with db.session() as session:
        query = session.query(StepsModel).filter(
            StepsModel.owner_id == uid, StepsModel.name == namerule
        )
        steps = query.first()
        if steps:
            session.delete(steps)
            try:
                session.commit()
                logger.info("StepsModel deleted successfully")
                return CeleryResponse(value="StepsModel deleted successfully").dict()
            except SQLAlchemyError as e:
                logger.error(f"Database delete operation failed: {str(e)}")
                return CeleryResponse(
                    error=f"Database delete operation failed: {str(e)}"
                ).dict()
        else:
            return CeleryResponse(error="Rule not found.").dict()


@shared_task(name="main.getsteps")
def getsteps(owner_id: str, namerule: str):
    try:
        uid = UUIDGenerator.generate(owner_id)
    except ValueError as ve:
        logger.error(f"Invalid UUID format: {str(ve)}")
        return CeleryResponse(error=f"Invalid UUID format: {str(ve)}").dict()

    with db.session() as session:
        query = session.query(StepsModel.steps).filter(
            StepsModel.owner_id == uid, StepsModel.name == namerule
        )
        steps_data = query.first()
        if steps_data:
            steps_dict = dict(steps_data.steps) if steps_data.steps else {}
            yaml_dump = yaml.dump(
                steps_dict, default_flow_style=False, allow_unicode=True
            )
            return CeleryResponse(value=yaml_dump).dict()
        else:
            return CeleryResponse(error="Rule not found.").dict()


@shared_task(name="main.liststeps")
def liststeps(owner_id: str):
    try:
        uid = UUIDGenerator.generate(owner_id)
    except ValueError as ve:
        logger.error(f"Invalid UUID format: {str(ve)}")
        return CeleryResponse(error=f"Invalid UUID format: {str(ve)}").dict()

    with db.session() as session:
        query = (
            session.query(StepsModel.name).filter(StepsModel.owner_id == uid).distinct()
        )
        steps_names = [rule_name for (rule_name,) in query]
        if steps_names:
            return CeleryResponse(value=steps_names).dict()
        else:
            return CeleryResponse(error="No steps found.").dict()


@shared_task(name="main.loadsteps")
def loadsteps(owner_id: str, namerule: str, rule: str):
    try:
        data = yaml.load(rule, Loader=hashcat_step_loader())
        model = parse_obj_as(Steps, data)
    except yaml.YAMLError as ye:
        logger.error(f"Failed to load YAML content: {str(ye)}")
        return CeleryResponse(error=f"Failed to load YAML content: {str(ye)}").dict()
    except ValidationError as ve:
        logger.error(f"Validation error for the provided data: {str(ve)}")
        return CeleryResponse(
            error=f"Validation error for the provided data: {str(ve)}"
        ).dict()

    steps_json = model.json()

    with db.session() as session:
        new_step = StepsModel(
            owner_id=UUIDGenerator.generate(owner_id),
            name=namerule,
            steps=json.loads(steps_json),
        )
        session.add(new_step)
        try:
            session.commit()
            logger.info("StepsModel saved successfully")
            return CeleryResponse(value="StepsModel saved successfully").dict()
        except SQLAlchemyError as e:
            logger.error(f"Database save operation failed: {str(e)}")
            return CeleryResponse(
                error=f"Database save operation failed: {str(e)}"
            ).dict()
