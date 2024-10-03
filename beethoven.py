import discord
from discord.ext import commands
import yt_dlp 
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = { 'options' : '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplayist':'True'}

class Beethoven(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
    

    @commands.command()
    async def play(self, ctx, url):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("You need to be in a voice channel to use this command!")
        
        if not ctx.voice_client:
            await voice_channel.connect()
        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url, title))
                await ctx.send(f"Added to queue: **{title}**")
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)         
        
        async def play_next(self, ctx):
            if 