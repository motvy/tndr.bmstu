import sys, os

import match_bot
import setting_bot

scriptDir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
sys.path.append(scriptDir+'/..')
sys.path.append(scriptDir)

import asyncio

async def main():
    if __name__ == '__main__':
        print("START")
        await asyncio.gather(setting_bot.main(),
                             match_bot.main(),)
asyncio.run(main())
