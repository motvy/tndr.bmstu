import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

import asyncio

from aiogram import Bot, Dispatcher

from aioredis import Redis
from aiogram.fsm.storage.redis import RedisStorage

import config
from setting_handlers import common, login, profile

from tndrlib import common as log


# Запуск бота
async def main():
    bot = Bot(token=config.settings_bot_settings['TOKEN'])

    redis = Redis()

    dp = Dispatcher(storage=RedisStorage(redis=redis))

    log.log_info('Connect settings log')

    dp.include_router(common.router)
    log.log_info('Load settings common')
    dp.include_router(login.router)
    log.log_info('Load settings login')
    dp.include_router(profile.router)
    log.log_info('Load settings profile')

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    log.log_info('Start settings bot')
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.log_info('Stop settings bot')
