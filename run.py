import json
<<<<<<< Updated upstream
from beethoven.bot import bot
=======
import asyncio
from botassets.bot import bot, setup
>>>>>>> Stashed changes

# Load config
with open("config.json") as f:
    config = json.load(f)

# Run the bot
bot.run(config["DISCORD_TOKEN"])
