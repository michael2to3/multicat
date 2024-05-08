import json
import logging
from uuid import UUID

import yaml
from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from exc import StepNotFoundError
from models import Step
from schemas import StepsList

logger = logging.getLogger(__name__)


class StepRetriever:
    def __init__(self, user_id: UUID, session: scoped_session):
        self._dbh = DatabaseHelper(session)
        self._session = session
        self._user_id = user_id

    def get_steps(self, step_name: str) -> str:
        step = (
            self._session.query(Step)
            .filter(
                Step.user_id == self._user_id,
                Step.name == step_name,
            )
            .first()
        )
        if not step:
            raise StepNotFoundError("Step not found.")
        hashcat_steps = [json.loads(s.value) for s in step.hashcat_steps]
        return yaml.dump(hashcat_steps, default_flow_style=False, allow_unicode=True)

    def get_orig_steps(self, step_name: str) -> str:
        original_content = (
            self._session.query(Step.original_content)
            .filter(
                Step.user_id == self._user_id,
                Step.name == step_name,
            )
            .first()
        )
        if not original_content:
            raise StepNotFoundError("Step not found.")
        return str(original_content[0])

    def get_steps_names(self) -> list[StepsList]:
        user = self._dbh.get_or_create_user(self._user_id)
        steps = (
            self._session.query(Step.name, Step.status, Step.timestamp)
            .filter(Step.user_id == user.id)
            .all()
        )
        return (
            [
                StepsList(name=step.name, status=step.status, timestamp=step.timestamp)
                for step in steps
            ]
            if steps
            else []
        )
