from commands import BaseCommand
from aiogram.types import Message
from .register_command import register_command

@register_command
class Hash(BaseCommand):
    @property
    def command(self):
        return "hash"

    @property
    def description(self):
        return "start brute force"

    async def handle(self, message: Message):
        hash_value = message.text
        result = self.app.send_task(
            "tasks.process_hash.process_hash", args=[[hash_value]], queue="server"
        )
        processing_result = result.get(timeout=10)
        await message.answer(f"{hash_value}: {processing_result}")
