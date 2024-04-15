import asyncio
import logging
from datetime import datetime, timedelta
from functools import wraps

from aiogram import types

from .message_wrapper import MessageWrapper
from .state_manager import StateManager

logger = logging.getLogger(__name__)


def fetched(interval: int = 3, timeout: int = 6 * 60 * 60, cool_down: int = 10):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, message: types.Message, *args, **kwargs) -> None:
            user_id = message.from_user.id
            now = datetime.now()
            last_execution = StateManager.get_last_execution(user_id)

            if last_execution and (now - last_execution) < timedelta(seconds=cool_down):
                await message.reply(
                    "Please wait a bit before using this command again."
                )
                return
            wrapped_message = MessageWrapper(self.bot, message)

            end_time = datetime.now() + timedelta(seconds=timeout)

            StateManager.reset_state(message.from_user.id)
            await func(self, wrapped_message, *args, **kwargs)

            StateManager.set_last_execution(user_id, now)

            await _repeated_execution_until_timeout(
                self, func, wrapped_message, end_time, interval, *args, **kwargs
            )

        async def _repeated_execution_until_timeout(
            self, func, message, end_time, interval, *args, **kwargs
        ):
            try:
                while datetime.now() < end_time and StateManager.has_command(
                    message.from_user.id
                ):
                    await func(self, message, *args, **kwargs)
                    await asyncio.sleep(interval)
            finally:
                StateManager.reset_state(message.from_user.id)

        return wrapper

    return decorator
