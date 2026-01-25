import asyncio
import os
import logging as log
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from handlers.startH import start
from handlers.psychology import psychology_router
from database.engine import create_db, drop_db, session_maker
from middlewares.mw import DataBaseSession

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    print('Бот лег')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_routers(start, psychology_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')