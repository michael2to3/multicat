import gnupg
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
        gpg = gnupg.GPG()

        key_identifier = "muclicat@deiteriy.com"
        public_keys = gpg.export_keys(key_identifier)

        if public_keys:
            document = BufferedInputFile(
                public_keys.encode("utf-8"), filename="public_key.asc"
            )
            await message.answer_document(document=document)
        else:
            await message.answer("Couldn't find my public GPG key.")
