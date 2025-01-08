import json
import asyncio
from assets.bot import bot, setup

# Load config
with open("config.json") as f:
    config = json.load(f)

async def main():
    async with bot:
        await setup()
        await bot.start(config["DISCORD_TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
