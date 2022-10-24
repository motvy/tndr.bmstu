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
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()

    dp.include_router(common.router)
    print("[INFO] load common")
    dp.include_router(login.router)
    print("[INFO] load login")
    dp.include_router(profile.router)
    print("[INFO] load profile")

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    print("[INFO] start bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
