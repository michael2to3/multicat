import logging
from uuid import UUID

from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from exc.steps import StepNotFoundError
from models import Step

logger = logging.getLogger(__name__)


class StepDeleter:
    def __init__(self, user_id: UUID, session: scoped_session):
        self._dbh = DatabaseHelper(session)
        self._session = session
        self._user_id = user_id

    def delete_step(self, step_name: str):
        user = self._dbh.get_or_create_user(self._user_id)
        step = self._get_step(user.id, step_name)
        if not step:
            raise StepNotFoundError("Step not found.")
        self._session.delete(step)

    def _get_step(self, user_id, step_name):
        return (
            self._session.query(Step)
            .filter(Step.name == step_name, Step.user_id == user_id)
            .first()
        )
