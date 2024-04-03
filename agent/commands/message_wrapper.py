import logging

from aiogram import Bot, types
from aiogram.exceptions import TelegramAPIError

from .state_manager import StateManager

logger = logging.getLogger(__name__)


class MessageWrapper:
    def __init__(self, bot: Bot, message: types.Message):
        self._bot = bot
        self._message = message

    async def answer(self, text: str, *args, **kwargs):
        user_id = self._message.from_user.id
        if StateManager.has_command(user_id):
            if StateManager.has_last_message_text(user_id, text):
                logger.info("Message has already been sent")
                return
            if await self._try_edit_last_message(text, user_id, *args, **kwargs):
                return
        await self._send_new_message(text, user_id, *args, **kwargs)

    async def _try_edit_last_message(self, text: str, user_id: int, *args, **kwargs):
        try:
            await self._bot.edit_message_text(
                text,
                chat_id=self._message.chat.id,
                message_id=StateManager.get_command_message_id(user_id),
                *args,
                **kwargs,
            )
            StateManager.set_last_message_text(user_id, text)
            return True
        except TelegramAPIError as e:
            logger.error("Failed to edit message: %s", e)
            return False

    async def _send_new_message(self, text: str, user_id: int, *args, **kwargs):
        new_message = await self._bot.send_message(
            chat_id=self._message.chat.id, text=text, *args, **kwargs
        )
        StateManager.add_command(user_id, new_message.message_id)
        StateManager.set_last_message_text(user_id, text)

    def __getattr__(self, item):
        return getattr(self._message, item)
