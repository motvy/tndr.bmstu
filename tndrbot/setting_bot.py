import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

import asyncio

from aiogram import Bot, Dispatcher

import config
from handlers import common, login, profile

from tndrlib import common as log


# Запуск бота
async def main():
    bot = Bot(token=config.settings_bot_settings['TOKEN'])
    dp = Dispatcher()

    log.log_init('main')
    log.log_info('Connect log')

    dp.include_router(common.router)
    log.log_info('Load common')
    dp.include_router(login.router)
    log.log_info('Load login')
    dp.include_router(profile.router)
    log.log_info('Load profile')

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    log.log_info('Start bot')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
