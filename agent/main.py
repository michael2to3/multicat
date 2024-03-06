import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router
from celery import Celery
import config
import celeryconfig
from commands import Hash, Start, Help

logging.basicConfig(level=logging.INFO)


bot = Bot(config.TELEGRAM_TOKEN)

app = Celery("agent")
app.config_from_object(celeryconfig)


async def main() -> None:
    dispatcher = Dispatcher()
    router = Router()
    Start(bot, router, app)
    Hash(bot, router, app)
    Help(bot, router, app)
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
