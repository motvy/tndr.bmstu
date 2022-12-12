import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

from tndrlib import common as log
from tndrlib.conn import Database

import asyncio

from aiogram import Bot, Dispatcher

from aioredis import Redis
from aiogram.fsm.storage.redis import RedisStorage

import config
from match_handlers import common, swipe, places


# Запуск бота
async def main():
    bot = Bot(token=config.match_bot_settings['TOKEN'])

    redis = Redis()
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    log.log_info('Connect match log')

    dp.include_router(common.router)
    log.log_info('Load match common')
    dp.include_router(swipe.router)
    log.log_info('Load match swipe')
    dp.include_router(places.router)
    log.log_info('Load match places')

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)

    Database().connect_matchdb()

    log.log_info('Start match bot')
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.log_info('Stop match bot')