from commands import BaseCommand
from aiogram.types import Message
from .register_command import register_command

@register_command
class Rules(BaseCommand):
    @property
    def command(self):
        return "rules"

    @property
    def description(self):
        return "Get rules from each client"

    async def handle(self, message: Message):
        result = self.app.send_task("main.get_rules", queue="server")
        processing_result = result.get(timeout=10)
        await message.answer(f"{processing_result}")
