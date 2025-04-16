import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import router
from logger import setup_logger

setup_logger()

async def main():
    bot = Bot(token='')  
    dp = Dispatcher(bot)
    dp.include_router(router)
    try:
        await dp.start_polling()
        logging.info('Бот запущен и готов к работе.')
    except Exception as e:
        logging.exception('Произошла ошибка при запуске бота: %s', e)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.exception('Произошла ошибка.')
        print('Бот выключен')
