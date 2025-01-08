import discord
from discord.ext import commands
<<<<<<< Updated upstream:beethoven/bot.py

# Create the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
=======
import os
import json

# Load config
with open("config.json") as f:
    config = json.load(f)

# Set up the bot with all intents and application id
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=config["APPLICATION_ID"]
)
>>>>>>> Stashed changes:botassets/bot.py

# I am back! (This is a comment)
@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected and ready!")

<<<<<<< Updated upstream:beethoven/bot.py
# Prefix command: !ping
@bot.command(name="ping")
async def ping_prefix(ctx):
    await ctx.send("Pong! (Prefix)")

# Slash command: /ping
@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! (Slash)")

# setup_hook is a special method that is called when the bot is starting up.
# It is necessary to sync the slash commands with Discord so that they are registered and available for use.
@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("Slash commands synced!")
=======
# Load all commands dynamically from the commands folder
async def load_commands():
    for filename in os.listdir("./botassets/commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"botassets.commands.{filename[:-3]}")
                print(f"Loaded extension {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {filename[:-3]}: {e}")

async def setup():
    await load_commands()
    await bot.load_extension("botassets.slash_commands")
>>>>>>> Stashed changes:botassets/bot.py

