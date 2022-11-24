import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

from tndrlib import common as log

import asyncio

from aiogram import Bot, Dispatcher

import config
from match_handlers import common


# Запуск бота
async def main():
    bot = Bot(token=config.match_bot_settings['TOKEN'])
    dp = Dispatcher()

    log.log_info('Connect match log')

    dp.include_router(common.router)
    log.log_info('Load match common')

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    log.log_info('Start match bot')
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.log_info('Stop match bot')