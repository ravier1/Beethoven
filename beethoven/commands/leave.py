import discord
from discord.ext import commands

@commands.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bye Bye!")
    else:
        await ctx.send("I'm not connected to any voice channel.")
