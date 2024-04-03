import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)


class UserState:
    def __init__(self):
        self.active_command: str = ""
        self.last_message_text: str = ""
        self.last_execution: datetime = datetime.min


class StateManager:
    _states: Dict[str, UserState] = {}

    @classmethod
    def add_command(cls, user_id: str, command: str):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.active_command = command
        logger.info(f"Command added for user {user_id} with command {command}")

    @classmethod
    def remove_command(cls, user_id: str):
        user_state = cls._get_or_create_user_state(user_id)
        if user_state.active_command:
            logger.info(
                f"Command '{user_state.active_command}' removed for user {user_id}"
            )
            user_state.active_command = ""
        else:
            logger.info(
                f"Tried to remove command for user {user_id}, but none was found"
            )

    @classmethod
    def get_command_message_id(cls, user_id: str) -> str:
        user_state = cls._get_or_create_user_state(user_id)
        return user_state.active_command

    @classmethod
    def has_command(cls, user_id: str) -> bool:
        user_state = cls._get_or_create_user_state(user_id)
        return bool(user_state.active_command)

    @classmethod
    def set_last_message_text(cls, user_id: str, text: str):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.last_message_text = text
        logger.info(f"Last message text set for user {user_id}")

    @classmethod
    def has_last_message_text(cls, user_id: str, text: str) -> bool:
        user_state = cls._get_or_create_user_state(user_id)
        return user_state.last_message_text == text

    @classmethod
    def set_last_execution(cls, user_id: str, execution_time: datetime):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.last_execution = execution_time
        logger.info(f"Last execution time set for user {user_id}: {execution_time}")

    @classmethod
    def get_last_execution(cls, user_id: str) -> datetime:
        user_state = cls._get_or_create_user_state(user_id)
        return user_state.last_execution

    @classmethod
    def reset_state(cls, user_id: str):
        if user_id in cls._states:
            del cls._states[user_id]
            logger.info(f"State reset for user {user_id}")
        else:
            logger.info(f"No state found to reset for user {user_id}")

    @classmethod
    def remove_last_message_text(cls, user_id: str):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.last_message_text = ""
        logger.info(f"Last message text removed for user {user_id}")

    @classmethod
    def _get_or_create_user_state(cls, user_id: str) -> UserState:
        if user_id not in cls._states:
            cls._states[user_id] = UserState()
        return cls._states[user_id]
