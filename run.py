from aiogram import Bot, Dispatcher
from config import TOKEN
import logging
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router

async def main():

    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot session ended ')
