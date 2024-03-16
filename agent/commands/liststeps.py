from aiogram.types import Message, ContentType
from aiogram.types.input_file import BufferedInputFile
from commands import BaseCommand
from .register_command import register_command


@register_command
class ListSteps(BaseCommand):
    @property
    def command(self):
        return "liststeps"

    @property
    def description(self):
        return "View avaliable steps for hashcat"

    async def handle(self, message: Message):
        userid = str(message.from_user.id)
        result = self.app.send_task("main.liststeps", args=(userid,), queue="server")
        processing_result = result.get(timeout=10)
        pretty_message_result = "\n".join(f"- {step}" for step in processing_result)
        await message.answer(
            f"Your saved rules:\n{pretty_message_result}\nYou can download rule with command /getsteps NAME"
        )
