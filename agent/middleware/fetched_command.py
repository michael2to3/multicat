import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from commands import StateManager

logger = logging.getLogger(__name__)


class FetchedCommandMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.message.from_user.id

        StateManager.remove_command(user_id)
        StateManager.remove_last_message_text(user_id)

        return await handler(event, data)
