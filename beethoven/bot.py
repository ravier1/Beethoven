import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord!")

#Mamma Mia! Please work!
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

