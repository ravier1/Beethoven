import discord
from discord.ext import commands

class JoinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Joined {channel.name}!")
        else:
            await ctx.send("You need to be in a voice channel to use this command.")

async def setup(bot):
    await bot.add_cog(JoinCommand(bot))