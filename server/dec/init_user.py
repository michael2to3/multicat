"""
This module provides a decorator to initialize a user in the database before
executing a function. It ensures the presence of a valid user_id, either from
the function's positional arguments or keyword arguments, and performs
necessary database operations.

Functions:
    init_user(session_factory) -> Callable

Usage Example:
    @init_user(session_factory)
    def some_function(user_id: UUID, ...):
        # Function implementation
"""

import logging
from functools import wraps
from typing import Callable
from uuid import UUID

from db import DatabaseHelper
from schemas import CeleryResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def init_user(session_factory) -> Callable:
    """
    A decorator to initialize a user in the database before executing the
    decorated function.

    This decorator validates the presence and type of the user_id, which can
    be provided as either a positional argument or a keyword argument. If the
    user_id is valid, it initializes the user in the database. If user
    creation fails, it logs the error and returns a CeleryResponse with an
    error message.

    Args:
        session_factory: A SQLAlchemy session factory used to create a new
        database session.

    Returns:
        A callable decorator that wraps the original function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrap(*args, **kwargs) -> Callable:
            user_id: UUID | None = None

            if len(args) >= 1 and isinstance(args[0], UUID):
                user_id = args[0]
            elif "user_id" in kwargs and isinstance(kwargs["user_id"], UUID):
                user_id = kwargs["user_id"]

            if user_id is None:
                raise ValueError("No valid user id provided")

            logger.debug("User id to init: %s", user_id)

            with session_factory() as session:
                dbh = DatabaseHelper(session)
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
