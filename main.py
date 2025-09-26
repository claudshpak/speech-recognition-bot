import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import router
from logger import setup_logger

load_dotenv()

setup_logger()

async def main():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logging.error("BOT_TOKEN не установлен!")
        return
    
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    
    try:
        logging.info('Бот запущен и готов к работе.')
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception('Произошла ошибка при запуске бота: %s', e)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')