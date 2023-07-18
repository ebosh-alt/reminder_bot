import asyncio
import sys

sys.path.append('D:/telegram_bots/reminder_bot')
from bot.utils.sheets import GetSheet, SendReminder


from contextlib import suppress
import logging
from bot.handlers import routers
from bot.config import bot, dp


async def main() -> None:
    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filemode="w",
                        format="%(levelname)s %(asctime)s %(message)s",
                        encoding='utf-8')

    with suppress(KeyboardInterrupt):

        parser = GetSheet()
        sender = SendReminder()
        parser.start_process(func=parser.start_schedule)
        sender.start_process(func=sender.start_schedule)
        asyncio.run(main())