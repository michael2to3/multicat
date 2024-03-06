from typing import Dict
from celery import Celery
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router
from abc import ABC, abstractmethod, abstractproperty


class BaseCommand(ABC):
    commands_info: Dict[str, str] = {}

    def __init__(self, bot: Bot, router: Router, app: Celery):
        self.bot = bot
        self.router = router
        self.app = app
        BaseCommand.commands_info[self.command] = self.description
        self.register_command_handler()

    @abstractproperty
    def description(self):
        pass

    @abstractproperty
    def command(self):
        pass

    @abstractmethod
    def handle(self, message: Message):
        pass

    def register_command_handler(self):
        @self.router.message(Command(self.command))
        async def inner_command_handler(message: Message):
            await self.handle(message)
