from aiogram.types.input_file import BufferedInputFile
from aiogram.types import Message
from commands import BaseCommand
from .register_command import register_command


@register_command
class PubKey(BaseCommand):
    @property
    def command(self):
        return "pubkey"

    @property
    def description(self):
        return "Get the bot's public GPG key."

    async def handle(self, message: Message):
        result = self.app.send_task(
            "main.get_pubkey", queue="server"
        )
        public_keys = result.get(timeout=60)
        if public_keys:
            document = BufferedInputFile(
                public_keys, filename="public_key.asc"
            )
            await message.answer_document(document=document)
        else:
            await message.answer("Couldn't find my public GPG key.")
