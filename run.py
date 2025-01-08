import json
import asyncio
from botassets.bot import bot, setup

# Load config
with open("config.json") as f:
    config = json.load(f)

# Run the bot
bot.run(config["DISCORD_TOKEN"])
