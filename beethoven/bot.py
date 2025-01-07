import discord
from discord.ext import commands

# Create the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot ready
@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected and ready!")

# Slash command: /ping
@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Sync application commands (slash commands)
@bot.event
async def setup_hook():
    # This ensures the slash commands are registered globally
    await bot.tree.sync()
    print("Slash commands synced!")

