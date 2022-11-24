import sys, os

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

from match_bot import match_bot
from setting_bot import setting_bot

from tndrlib import common as log


import asyncio

log.log_init('main')

async def main():
    await asyncio.gather(setting_bot.main(), match_bot.main())

try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    log.log_info("Stop bots")

