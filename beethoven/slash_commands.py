import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import shutil
from discord import FFmpegPCMAudio

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="join", description="Joins your voice channel.")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel.name}!")
        else:
            await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)

    @app_commands.command(name="leave", description="Leaves the voice channel.")
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Disconnected from the voice channel.")
        else:
            await interaction.response.send_message("I'm not connected to any voice channel.", ephemeral=True)

    @app_commands.command(name="play", description="Plays a song from YouTube.")
    async def play(self, interaction: discord.Interaction, url: str):
        if not interaction.guild.voice_client:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                await channel.connect()
                await interaction.response.send_message(f"Joined {channel.name}!")
            else:
                await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
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
            await interaction.response.send_message(
                "FFMPEG is required to run this bot. Please install it and ensure it's added to your PATH.",
                ephemeral=True,
            )
            return

        vc = interaction.guild.voice_client
        await interaction.response.send_message("Fetching audio...")

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        vc.stop()
        audio = FFmpegPCMAudio(audio_url, executable=ffmpeg_path, **FFMPEG_OPTIONS)
        volume_transformer = PCMVolumeTransformer(audio, volume=self.bot.get_cog("VolumeCommand")._volume)
        vc.play(volume_transformer)
        await interaction.followup.send(f"Now playing: {info['title']}")

    @app_commands.command(name="ping", description="Replies with Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="volume", description="Set the volume (0-100)")
    async def volume(self, interaction: discord.Interaction, volume: int = None):
        volume_cog = self.bot.get_cog("VolumeCommand")
        if volume is None:
            current = int(volume_cog._volume * 100)
            await interaction.response.send_message(f"Current volume: {current}%")
            return
            
        if not 0 <= volume <= 100:
            await interaction.response.send_message("Volume must be between 0 and 100")
            return

        volume_cog._volume = volume / 100.0
        
        if interaction.guild.voice_client and interaction.guild.voice_client.source:
            interaction.guild.voice_client.source.volume = volume_cog._volume
            
        await interaction.response.send_message(f"Volume set to {volume}%")

# Add the cog
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
