from aiogram.types import Message

from commands import BaseCommand
from dec import register_command
from state import MessageWrapper


@register_command
class Start(BaseCommand):
    @property
    def command(self):
        return "start"

    @property
    def description(self):
        return "Start the bot and get a welcome message"

    async def handle(self, message: Message | MessageWrapper):
        await message.answer("Hi! Can u give me some hashes?")
