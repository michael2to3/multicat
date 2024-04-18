import logging
from datetime import datetime, timedelta
from uuid import UUID

import yaml
from pydantic import ValidationError

from db import DatabaseHelper
from models.hashcat_request import StepStatus
from schemas import Steps, hashcat_step_loader
from steps import StepDeleter
from steps.loader import KeyspaceCalculator, StepLoader

logger = logging.getLogger(__name__)


class StepLoadFacade:
    def __init__(self, user_id: UUID, session):
        self._user_id = user_id
        self._session = session
        self._dbh = DatabaseHelper(session)
        self._step_loader = StepLoader(user_id, session)
        self._step_deleter = StepDeleter(user_id, session)
        self._keyspace_calculator = KeyspaceCalculator(self._dbh, session, user_id)

    def process_steps(self, steps_name: str, yaml_content: str):
        try:
            data = hashcat_step_loader().load(yaml_content)
            steps = Steps(**data)
        except (yaml.YAMLError, ValidationError) as e:
            logger.error(f"Error loading and validating steps: {str(e)}")
            raise
        except TypeError as e:
            logger.error("Failed to instantiate steps: %s", str(e))
            logger.debug("Data received: %s", yaml_content)
            raise

        try:
            steps_last = self._dbh.get_steps(self._user_id, steps_name)
            if datetime.now() - steps_last.timestamp > timedelta(minutes=10):
                self._step_deleter.delete_step(steps_name)
                self._session.commit()
                raise ValueError
            return self.handle_existing_steps(steps_last)
        except ValueError:
            return self.load_new_steps(steps_name, steps, yaml_content)

    def handle_existing_steps(self, steps_last):
        match steps_last.status:
            case StepStatus.SUCCESS.value:
                return "Steps loaded successfully"
            case StepStatus.FAILED.value:
                return "Failed to load your steps"
            case StepStatus.PROCESSING.value:
                return "Processing..."
            case _:
                return "Unknown status ;/"

    def load_new_steps(self, steps_name, steps, yaml_content):
        self._step_loader.load_steps(steps_name, steps, yaml_content)
        self._session.commit()
        self._keyspace_calculator.calculate_and_save_unknown_keyspaces(
            steps, steps_name
        )
        return "Steps loaded and processed"
