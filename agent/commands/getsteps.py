from io import BytesIO
from aiogram.types import Message, ContentType
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from .register_command import register_command


@register_command
class GetSteps(BaseCommand):
    @property
    def command(self):
        return "getsteps"

    @property
    def description(self):
        return "Download Steps for hashcat"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        text_message = " ".join(message.text.split(" ")[1:])
        if not text_message:
            await message.answer("Please enter step name")
            return

        result = self.app.send_task(
            "main.getsteps", args=(userid, text_message), queue="server"
        )
        processing_result = result.get(timeout=10)

        document = BufferedInputFile(
            processing_result.encode("UTF-8"), filename=text_message
        )
        await message.answer_document(document=document)
