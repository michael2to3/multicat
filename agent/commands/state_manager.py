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
    _states: Dict[int, UserState] = {}

    @classmethod
    def add_command(cls, user_id: int, command: str):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.active_command = command
        logger.info("Command added for user %s with command %s", user_id, command)

    @classmethod
    def remove_command(cls, user_id: int):
        user_state = cls._get_or_create_user_state(user_id)
        if user_state.active_command:
            logger.info(
                "Command '%s' removed for user %s", user_state.active_command, user_id
            )
            user_state.active_command = ""
        else:
            logger.info("Tried to remove command for user %s", user_id)

    @classmethod
    def get_command_message_id(cls, user_id: int) -> str:
        user_state = cls._get_or_create_user_state(user_id)
        return user_state.active_command

    @classmethod
    def has_command(cls, user_id: int) -> bool:
        user_state = cls._get_or_create_user_state(user_id)
        return bool(user_state.active_command)

    @classmethod
    def set_last_message_text(cls, user_id: int, text: str):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.last_message_text = text
        logger.info("Last message text set for user %s: %s", user_id, text)

    @classmethod
    def has_last_message_text(cls, user_id: int, text: str) -> bool:
        user_state = cls._get_or_create_user_state(user_id)
        return user_state.last_message_text == text

    @classmethod
    def set_last_execution(cls, user_id: int, execution_time: datetime):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.last_execution = execution_time
        logger.info("Last execution time set for user %s: %s", user_id, execution_time)

    @classmethod
    def get_last_execution(cls, user_id: int) -> datetime:
        user_state = cls._get_or_create_user_state(user_id)
        return user_state.last_execution

    @classmethod
    def reset_state(cls, user_id: int):
        if user_id in cls._states:
            del cls._states[user_id]
            logger.info("State reset for user %s", user_id)
        else:
            logger.info("No state found to reset for user %s", user_id)

    @classmethod
    def remove_last_message_text(cls, user_id: int):
        user_state = cls._get_or_create_user_state(user_id)
        user_state.last_message_text = ""
        logger.info("Last message text removed for user %s", user_id)

    @classmethod
    def _get_or_create_user_state(cls, user_id: int) -> UserState:
        if user_id not in cls._states:
            cls._states[user_id] = UserState()
        return cls._states[user_id]
