import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router
from commands import command_registry
from config import CeleryApp, Config

logging.basicConfig(level=logging.INFO)


bot = Bot(Config.get("TELEGRAM_TOKEN"))
app = CeleryApp("agent").get_app()


async def main() -> None:
    dispatcher = Dispatcher()
    router = Router()

    for command_cls in command_registry.list_commands():
        command_cls(bot, router, app)

    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
