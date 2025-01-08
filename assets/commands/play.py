import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
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
            else:
                await ctx.send("You need to be in a voice channel to use this command.")
                return

        yt_dlp_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'no_warnings': True,
            'extract_audio': True,
            'audio_format': 'mp3',
            'default_search': 'auto',
        }

        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            await ctx.send("FFMPEG is required to run this bot. Please install it.")
            return

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': f'-vn -filter:a volume={self.bot.get_cog("VolumeCommand")._volume}'
        }

        try:
            vc = ctx.voice_client
            await ctx.send("Fetching audio...")

            with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']
                title = info.get('title', 'Unknown title')

            vc.stop()
            audio = FFmpegPCMAudio(url2, **FFMPEG_OPTIONS, executable=ffmpeg_path)
            volume_transformer = PCMVolumeTransformer(audio, volume=self.bot.get_cog("VolumeCommand")._volume)
            vc.play(volume_transformer)

            await ctx.send(f"Now playing: {title}")
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug print
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(PlayCommand(bot))
