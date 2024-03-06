import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from celery import Celery
import config
import celeryconfig

logging.basicConfig(level=logging.INFO)


bot = Bot(config.TELEGRAM_TOKEN)

app = Celery("agent")
app.config_from_object(celeryconfig)

router = Router()


@router.message(CommandStart())
async def send_welcome(message: Message) -> None:
    await message.answer(
        "Привет! Я Агент для отправки хешей на обработку. Отправь мне хеш для обработки."
    )


@router.message()
async def handle_hash(message: types.Message) -> None:
    hash_value = message.text
    logging.info(f"Hash received: {hash_value}")

    result = app.send_task("tasks.process_hash.process_hash", args=[[hash_value]])
    processing_result = result.get(timeout=10)

    await message.answer(f"Результат обработки хеша: {processing_result}")


async def main() -> None:
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
