from commands import BaseCommand
from aiogram.types import Message
from .register_command import register_command

@register_command
class Hashcat(BaseCommand):
    @property
    def command(self):
        return "hashcat"

    @property
    def description(self):
        return "Start attack!!1!1!11"

    async def handle(self, message: Message):
        result = self.app.send_task("main.run_hashcat", queue="server")
        processing_result = result.get(timeout=10)
        await message.answer(f"{processing_result}")
