import discord
from discord.ext import commands
import os

# Set up the bot with all intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is connected and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Load all commands dynamically from the commands folder
async def load_commands():
    for filename in os.listdir("./assets/commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"assets.commands.{filename[:-3]}")
                print(f"Loaded extension {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {filename[:-3]}: {e}")

async def setup():
    await load_commands()
    await bot.load_extension("assets.slash_commands")

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(setup())
