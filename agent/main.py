import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router
from commands import command_registry
from config import CeleryApp, Config
from middleware import FetchedCommandMiddleware

config = Config()
bot = Bot(config.telegram_token)
app = CeleryApp("agent").get_app()

def logger_setup() -> None:
    logger_level = getattr(logging, config.logger_level.upper(), logging.INFO)
    logging.basicConfig(level=logger_level)

async def main() -> None:
    dispatcher = Dispatcher()
    router = Router()

    dispatcher.update.outer_middleware(FetchedCommandMiddleware())

    for command_cls in command_registry.list_commands():
        command_cls(bot, router, app)

    dispatcher.include_router(router)
    await dispatcher.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logger_setup()
    asyncio.run(main())
