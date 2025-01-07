import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
import shutil

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx, url: str):
        if not ctx.voice_client:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send(f"Joined {channel.name}!")
            else:
                await ctx.send("You need to be in a voice channel to use this command.")
                return

        yt_dlp_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            await ctx.send("FFMPEG is required to run this bot. Please install it.")
            return

        vc = ctx.voice_client
        await ctx.send("Fetching audio...")

        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        vc.stop()
        vc.play(
            FFmpegPCMAudio(audio_url, executable=ffmpeg_path),
            after=lambda e: print(f"Finished playing: {e}"),
        )
        await ctx.send(f"Now playing: {info['title']}")

async def setup(bot):
    await bot.add_cog(PlayCommand(bot))
