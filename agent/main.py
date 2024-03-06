import logging
from aiogram import Bot, Dispatcher, executor, types
from celery import Celery
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

app = Celery("agent", broker="amqp://guest:guest@localhost")
app.config_from_object("celeryconfig")


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я Агент для отправки хешей на обработку. Отправь мне хеш для обработки."
    )


@dp.message_handler()
async def handle_hash(message: types.Message):
    hash_value = message.text
    logging.info(f"Получен хеш: {hash_value}")

    result = app.send_task("server.process_hashes", args=[[hash_value]])
    processing_result = result.get(timeout=10)

    await message.reply(f"Результат обработки хеша: {processing_result}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
