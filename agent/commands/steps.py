import logging

from aiogram.enums import ParseMode
from aiogram.types import ContentType, Message
from aiogram.types.input_file import BufferedInputFile

from commands import BaseCommand
from config.uuid import UUIDGenerator
from dec import register_command
from schemas import CeleryResponse, StepsList, StepStatus
from state import MessageWrapper, fetched

logger = logging.getLogger(__name__)


@register_command
class StepsListCommand(BaseCommand):
    @property
    def command(self) -> str:
        return "sl"

    @property
    def description(self) -> str:
        return "View all workflow steps"

    async def handle(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        result = self.app.send_task("server.list_steps", args=(userid,))
        celery_response = CeleryResponse(**result.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
            return
        response_message = "Your steps:\n"
        if celery_response.value:
            steps_list = sorted(
                [StepsList(**i) for i in celery_response.value],
                key=lambda x: x.timestamp,
            )
            response_message += "\n".join(
                f"{self._handle_steps_status(i.status)} - {i.name}" for i in steps_list
            )
        else:
            response_message += "No steps found."

        if celery_response.warning:
            response_message += f"\nWarning: {celery_response.warning}"

        await message.answer(response_message)
        return

    def _handle_steps_status(self, step_status: StepStatus) -> str:
        match step_status:
            case StepStatus.SUCCESS:
                return "✅"
            case StepStatus.PROCESSING:
                return "🔄"
            case StepStatus.FAILED:
                return "❌"
            case _:
                return "❓"


@register_command
class StepsGetCommand(BaseCommand):
    @property
    def command(self) -> str:
        return "sg"

    @property
    def description(self) -> str:
        return "Details of a step"

    async def handle(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        step_name = message.text.split(maxsplit=1)[1] if message.text else ""

        result = self.app.send_task("server.get_steps", args=(userid, step_name))
        celery_response = CeleryResponse(**result.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
            return
        if celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        if not celery_response.value:
            await message.answer("Step not found.")
            return

        step_details = celery_response.value
        document = BufferedInputFile(
            bytes(step_details, encoding="UTF-8"), filename=step_name
        )
        await message.answer_document(
            document=document, caption=f"Details for step '{step_name}':"
        )


@register_command
class StepsLoadCommand(BaseCommand):
    @property
    def command(self) -> str:
        return "slo"

    @property
    def description(self) -> str:
        return "Add/update steps via YAML file"

    @fetched(interval=15)
    async def handle(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        if message.content_type != ContentType.DOCUMENT:
            await message.answer("Please send a YAML file.")
            return

        document_id, file_name = message.document.file_id, message.document.file_name
        file_info = await self.bot.get_file(document_id)
        file_bytes = await self.bot.download_file(file_info.file_path)
        content = file_bytes.read().decode("UTF-8")

        result = self.app.send_task(
            "server.load_steps", args=(userid, file_name, content)
        )
        await self._process_celery_response(
            message, CeleryResponse(**result.get(timeout=60))
        )


@register_command
class StepsDeleteCommand(BaseCommand):
    @property
    def command(self) -> str:
        return "sd"

    @property
    def description(self) -> str:
        return "Remove a step"

    async def handle(self, message: Message | MessageWrapper):
        if not message.text:
            message.answer("Please provide the name of the step to delete.")

        userid = UUIDGenerator.generate(str(message.from_user.id))
        text = message.text if message.text else ""
        steps_name = text.split(maxsplit=1)[1]

        result = self.app.send_task("server.delete_steps", args=(userid, steps_name))
        return await self._process_celery_response(
            message, CeleryResponse(**result.get(timeout=60))
        )


@register_command
class StepsPrintCommand(BaseCommand):
    @property
    def command(self) -> str:
        return "sp"

    @property
    def description(self) -> str:
        return "Print the details of the steps"

    async def handle(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        text = message.text.split(maxsplit=1)[1] if message.text else ""

        result = self.app.send_task("server.get_orig_steps", args=(userid, text))
        celery_response = CeleryResponse(**result.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
            return
        if celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        if not celery_response.value:
            await message.answer("Step not found.")
            return

        step_details = celery_response.value
        await message.answer(
            f"```yaml\n{step_details}```", parse_mode=ParseMode.MARKDOWN_V2
        )


@register_command
class StepsOriginalCommand(BaseCommand):
    @property
    def command(self) -> str:
        return "so"

    @property
    def description(self) -> str:
        return "View original step configuration"

    async def handle(self, message: Message | MessageWrapper):
        userid = UUIDGenerator.generate(str(message.from_user.id))
        step_name = message.text.split(maxsplit=1)[1] if message.text else ""

        result = self.app.send_task("server.get_orig_steps", args=(userid, step_name))
        celery_response = CeleryResponse(**result.get(timeout=10))

        if celery_response.error:
            await message.answer(f"Error: {celery_response.error}")
            return
        if celery_response.warning:
            await message.answer(f"Warning: {celery_response.warning}")
        if not celery_response.value:
            await message.answer("Step not found.")
            return

        step_details = celery_response.value

        document = BufferedInputFile(
            bytes(step_details, encoding="UTF-8"), filename=step_name
        )
        await message.answer_document(
            document=document, caption=f"Details for step '{step_name}':"
        )
