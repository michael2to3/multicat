import json
import logging
from uuid import UUID

import yaml
from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from models import Step
from models.hashcat_request import StepStatus

logger = logging.getLogger(__name__)


class StepRetriever:
    def __init__(self, user_id: UUID, session: scoped_session):
        self._dbh = DatabaseHelper(session)
        self._session = session
        self._user_id = user_id

    def get_steps(self, step_name: str) -> str:
        step = self._get_step_with_keyspace(step_name)
        if not step:
            raise ValueError("Step not found.")
        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]
        return yaml.dump(hashcat_steps, default_flow_style=False, allow_unicode=True)

    def get_orig_steps(self, step_name: str) -> str:
        step = self._get_step_with_keyspace(step_name)
        if not step:
            raise ValueError("Step not found.")
        return str(step.original_content)

    def get_steps_names(self) -> list[str]:
        user = self._dbh.get_or_create_user(self._user_id)
        steps = self._session.query(Step.name, Step.status).filter(Step.user_id == user.id).all()
        return (
            [
                f"{self._handle_steps_status(step.status)} - {step.name}"
                for step in steps
            ]
            if steps
            else []
        )

    def _handle_steps_status(self, step_status: int) -> str:
        match step_status:
            case StepStatus.SUCCESS.value:
                return "✅"
            case StepStatus.PROCESSING.value:
                return "🔄"
            case StepStatus.FAILED.value:
                return "❌"
            case _:
                return "❓"

    def _get_step_with_keyspace(self, step_name):
        return (
            self._session.query(Step)
            .filter(
                Step.user_id == self._user_id,
                Step.name == step_name,
                Step.status == StepStatus.SUCCESS.value,
            )
            .first()
        )
