import discord
from discord.ext import commands

# Create the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# I am back! (This is a comment)
@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected and ready!")

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

