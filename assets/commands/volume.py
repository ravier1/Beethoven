import discord
from discord.ext import commands
from discord import PCMVolumeTransformer

class VolumeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._volume = 1.0  # 1.0 = 100%

    @commands.command(name="volume")
    async def volume(self, ctx, volume: int = None):
        if volume is None:
            current = int(self._volume * 100)
            await ctx.send(f"Current volume: {current}%")
            return
            
        if not 0 <= volume <= 100:
            await ctx.send("Volume must be between 0 and 100")
            return

        self._volume = volume / 100.0
        
        if ctx.voice_client and ctx.voice_client.source:
            ctx.voice_client.source.volume = self._volume
            
        await ctx.send(f"Volume set to {volume}%")

async def setup(bot):
    await bot.add_cog(VolumeCommand(bot))