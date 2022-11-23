import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

import match_bot
import setting_bot

from tndrlib import common as log


import asyncio

async def main():
    log.log_init('main')
    await asyncio.gather(setting_bot.main(), match_bot.main())

asyncio.run(main())

