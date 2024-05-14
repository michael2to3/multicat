import logging
from abc import ABC, abstractmethod
from typing import Dict

from aiogram import Bot
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message
from celery import Celery
from schemas import CeleryResponse

from .message_wrapper import MessageWrapper

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    commands_info: Dict[str, str] = {}

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
        self, message: Message, celery_response: CeleryResponse
    ):
        if celery_response.error:
            return await message.answer(f"Error: {celery_response.error}")
        elif celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        elif celery_response.value:
            await message.answer(f"{celery_response.value}")
        else:
            await message.answer("Operation completed successfully.")
