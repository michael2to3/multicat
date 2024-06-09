import logging
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable

from aiogram import Bot
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import ContentType, Message
from celery import Celery

from schemas import CeleryResponse
from state import MessageWrapper

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    commands_info: dict[str, str] = {}

    def __init__(self, bot: Bot, router: Router, app: Celery):
        self.bot = bot
        self.router = router
        self.app = app
        BaseCommand.commands_info[self.command] = self.description
        self.register_command_handler()

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def command(self) -> str:
        pass

    @abstractmethod
    async def handle(self, message: Message | MessageWrapper):
        pass

    def register_command_handler(self):
        @self.router.message(Command(self.command))
        async def inner_command_handler(message: Message):
            try:
                await self.handle(message)
            except Exception as e:
                logger.error(
                    "Error handling command %s: %s", self.command, e, exc_info=True
                )
                await message.reply("Something went wrong. Please try again later.")

    async def _process_celery_response(
        self,
        message: Message | MessageWrapper,
        celery_response: CeleryResponse,
        send_response: (
            Callable[[Message | MessageWrapper, Any], Awaitable] | None
        ) = None,
    ):
        if send_response is None:
            send_response = self._default_send_response

        if celery_response.error:
            return await message.answer(f"Error: {celery_response.error}")
        elif celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        elif celery_response.value:
            await send_response(message, celery_response.value)
        else:
            await message.answer("Operation completed successfully.")

    async def _default_send_response(
        self, message: Message | MessageWrapper, text: str
    ):
        await message.answer(text, parse_mode="Markdown")

    def _is_document_message(self, message: Message | MessageWrapper) -> bool:
        return (
            message.content_type == ContentType.DOCUMENT
            and message.document is not None
        )
