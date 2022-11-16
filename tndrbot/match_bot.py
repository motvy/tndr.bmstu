import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

import asyncio

from aiogram import Bot, Dispatcher

import config
from handlers import common, login, profile


# Запуск бота
async def main():
    bot = Bot(token=config.match_bot_settings['TOKEN'])
    dp = Dispatcher()

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    print("[INFO] start bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())