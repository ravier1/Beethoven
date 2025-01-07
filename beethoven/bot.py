import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp

# Create the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# YouTube options
yt_dlp_opts = {
    "format": "bestaudio/best",
    "quiet": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# I am back! (This is a comment)
@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected and ready!")

# Prefix command: !ping
@bot.command(name="ping")
async def ping_prefix(ctx):
    await ctx.send("Pong! (Prefix)")

# Slash command: /ping
@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


# Join voice channel
@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("You need to be in a voice channel for me to join.")


@bot.command(name="play")
async def play(ctx, url: str):
    # If the bot isn't connected, join the user's voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Joined {channel.name}!")
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

    vc = ctx.voice_client

    # Download and play audio
    await ctx.send("Fetching audio...")
    with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info["url"]

    vc.stop()  # Stop any currently playing audio
    vc.play(FFmpegPCMAudio(audio_url), after=lambda e: print(f"Finished playing: {e}"))
    await ctx.send(f"Now playing: {info['title']}")


# Leave voice channel
@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bye!")
    else:
        await ctx.send("I'm not connected to any voice channel.")


# setup_hook is a special method that is called when the bot is starting up.
# It is necessary to sync the slash commands with Discord so that they are registered and available for use.
@bot.event
async def setup_hook():
    await bot.tree.sync()
    print("Slash commands synced!")

