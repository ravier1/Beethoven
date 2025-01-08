import json
from beethoven.bot import bot

# Load config
with open("config.json") as f:
    config = json.load(f)

# Run the bot
bot.run(config["DISCORD_TOKEN"])
