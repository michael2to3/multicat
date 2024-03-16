from io import BytesIO
from aiogram.types import Message, ContentType
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from .register_command import register_command


@register_command
class GetSteps(BaseCommand):
    @property
    def command(self):
        return "delsteps"

    @property
    def description(self):
        return "Delete Steps for hashcat"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        text_message = " ".join(message.text.split(" ")[1:])
        if not text_message:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task(
            "main.delsteps", args=(userid, text_message), queue="server"
        )
        processing_result = result.get(timeout=10)

        await message.answer(f"{processing_result}")
