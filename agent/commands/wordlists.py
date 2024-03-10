from commands import BaseCommand
from aiogram.types import Message
from .register_command import register_command

@register_command
class Wordlists(BaseCommand):
    @property
    def command(self):
        return "wordlists"

    @property
    def description(self):
        return "Get wordlists from each client"

    async def handle(self, message: Message):
        result = self.app.send_task("main.get_wordlists", queue="server")
        processing_result = result.get(timeout=10)
        await message.answer(f"{processing_result}")
