import logging

from sqlalchemy.orm import scoped_session

from db import DatabaseHelper
from models import Step

logger = logging.getLogger(__name__)


class StepDeleter:
    def __init__(self, user_id: str, session: scoped_session):
        self.db_helper = DatabaseHelper(session)
        self.session = session
        self.user_id = user_id

    def delete_step(self, step_name: int):
        user = self.db_helper.get_or_create_user(self.user_id)
        step = self._get_step(user.id, step_name)
        if not step:
            raise ValueError("Step not found.")
        self.session.delete(step)

    def _get_step(self, user_id, step_name):
        return (
            self.session.query(Step)
            .filter(Step.name == step_name, Step.user_id == user_id)
            .first()
        )
