import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID


from db import DatabaseHelper
from exc.steps import StepNotFoundError
from schemas import Steps, StepStatus
from steps import StepDeleter
from steps.loader import KeyspaceCalculator, StepLoader
from yamlutils import yaml_step_loader

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
        data = yaml_step_loader().load(yaml_content)
        steps = Steps(**data)
        try:
            steps_last = self._dbh.get_steps(self._user_id, steps_name)
            if datetime.now(UTC) - steps_last.timestamp > timedelta(minutes=10):
                self._step_deleter.delete_step(steps_name)
                self._session.commit()
                raise StepNotFoundError
            return self.handle_existing_steps(steps_last)
        except StepNotFoundError:
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
