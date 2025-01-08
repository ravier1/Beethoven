import discord
from discord.ext import commands

class LeaveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Bye Bye!")
        else:
            await ctx.send("I'm not connected to any voice channel.")

async def setup(bot):
    await bot.add_cog(LeaveCommand(bot))