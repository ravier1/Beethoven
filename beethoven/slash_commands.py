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

        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        vc.stop()
        vc.play(
            FFmpegPCMAudio(audio_url, executable=ffmpeg_path),
            after=lambda e: print(f"Finished playing: {e}"),
        )
        await interaction.followup.send(f"Now playing: {info['title']}")

    @app_commands.command(name="ping", description="Replies with Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

# Add the cog
async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
