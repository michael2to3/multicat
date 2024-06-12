import json
import logging
from uuid import UUID

import yaml
from sqlalchemy.orm import joinedload, scoped_session

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

    def get_dump(self, step_name: str) -> str:
        steps = self._get_steps(step_name)
        hashcat_steps = [json.loads(hs.value) for s in steps for hs in s.hashcat_steps]
        return yaml.dump(hashcat_steps, default_flow_style=False, allow_unicode=True)

    def get_steps(self, step_name: str) -> list[Step]:
        return self._get_steps(step_name)

    def get_orig_dump(self, step_name: str) -> str:
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
            self._session.query(Step.name, Step.status, Step.created_at)
            .filter(Step.user_id == user.id)
            .all()
        )
        return (
            [
                StepsList(
                    name=step.name, status=step.status, created_at=step.created_at
                )
                for step in steps
            ]
            if steps
            else []
        )

    def _get_steps(self, step_name: str):
        step: list[Step] = (
            self._session.query(Step)
            .options(joinedload(Step.hashcat_steps))
            .filter(
                Step.user_id == self._user_id,
                Step.name == step_name,
            )
            .all()
        )
        if not step:
            raise StepNotFoundError("Step not found.")

        return step
