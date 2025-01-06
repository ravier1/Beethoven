import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord!")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

if __name__ == "__main__":
    bot.run("YOUR_DISCORD_TOKEN")
