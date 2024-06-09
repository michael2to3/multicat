from aiogram.types import Message

from commands import BaseCommand
from dec import register_command
from state import MessageWrapper


@register_command
class Help(BaseCommand):
    @property
    def command(self):
        return "help"

    @property
    def description(self):
        return "Print this message"

    async def handle(self, message: Message | MessageWrapper):
        help_message = "Available commands:\n"
        for command, description in BaseCommand.commands_info.items():
            help_message += f"/{command} - {description}\n"
        await message.answer(help_message)
