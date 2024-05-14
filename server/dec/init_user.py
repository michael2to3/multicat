import logging
from functools import wraps
from uuid import UUID

from db import DatabaseHelper
from schemas import CeleryResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def init_user(session_factory):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            logger.debug("Try to init user")
            if len(args) < 1:
                raise ValueError("No user id provided")
            if not isinstance(args[0], UUID):
                raise ValueError(
                    f"User id expected as UUID but got {type(args[0])} - {args[0]} in {func.__name__} function"
                )

            logger.debug("User id to init: %s", args[0])

            with session_factory() as session:
                dbh = DatabaseHelper(session)
                user_id: UUID = args[0]
                try:
                    _ = dbh.get_or_create_user(user_id)
                    logger.debug("User %s created successfully", user_id)
                except SQLAlchemyError as e:
                    logger.error("User creation failed: %s", e, exc_info=True)
                    session.rollback()
                    return CeleryResponse(error="User creation failed").model_dump()

            return func(*args, **kwargs)

        return wrap

    return decorator
