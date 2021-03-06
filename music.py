import os
from re import A
import discord
from discord.ext import commands
import youtube_dl 
from builtins import bot
import asyncio

q = {}

YDL_OPTIONS = {'format':'bestaudio'}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FMMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def addEntry(id):
    if id not in q:
        q[id] = []


@bot.command()
async def musicJoin(ctx):
    """Gets the music bot to join the voice channel the user is in. Usage: musicJoin"""
    if ctx.author.voice is None:
       await ctx.send("Join a voice channel before asking me to join")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    
@bot.command()
async def musicLeave(ctx):
    """Gets the music bot to leave the discord voice channel. Usage: musicLeave"""
    await ctx.voice_client.disconnect()
    
@bot.command()
async def playMusic(ctx,url):
    """Plays music or adds it to the queue to be played. Usage: playMusic https://www.youtube.com/watch?v=360c_SkOByI"""
    if ctx.author.voice is None:
       await ctx.send("Join a voice channel before asking me to join")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    vc = ctx.voice_client
    addEntry(ctx.guild.id)
    q[ctx.guild.id].append(url)
    print(f"PLAYING = {checkPlayings(ctx)}")
    if not checkPlayings(ctx):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(q[ctx.guild.id][0],download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FMMPEG_OPTIONS)
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx),bot.loop))

@bot.command()
async def musicSkip(ctx):
    ctx.voice_client.stop()
    await ctx.reply("Skipped")

async def play_next(ctx):
    if len(q[ctx.guild.id]) >= 1:
        del q[ctx.guild.id][0]
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(q[ctx.guild.id][0],download=False)
            url2 = info['formats'][0]['url']
            vc = ctx.voice_client
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FMMPEG_OPTIONS)
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx),bot.loop))
        asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue after this one."),bot.loop)

def checkPlayings(ctx):
    vc = ctx.voice_client
    return vc.is_playing()

# This command is used for testing purposes only
#@bot.command()
#async def checkPlaying(ctx):
#    """Checks if the music bot is playing. Usage: checkPlaying"""
#    await ctx.send(f"Playing = {checkPlayings(ctx)}")

@bot.command()
async def musicPause(ctx):
    """Pauses whatever the music bot is playing. Usage: musicPause"""
    try:
        await ctx.voice_client.pause()
    except:
        print("caught exception in musicPause")
    await ctx.send("Paused Music")

@bot.command()
async def musicResume(ctx):
    """Resumes if music bot is paused. Usage: musicResume"""
    try:
        await ctx.voice_client.resume()
    except:
        print("caught exception in musicResume")
    await ctx.send("Resumed Music")
        
@bot.command()
async def musicRemove(ctx,num):
    """Removes the url from the queue. Usage: musicRemove 1"""
    try:
        del(q[ctx.guild.id][int(num)])
        await ctx.send(f"Queue is {q[ctx.guild.id]}")
    except:
        await ctx.send("Error with removing from queue")

@bot.command()
async def musicQueue(ctx):
    """Prints the queue for the musicbot. Usage: musicQueue"""
    try:
        await ctx.send(f"Queue is {q[ctx.guild.id]}")
    except:
        await ctx.send(f"Queue is []")

@bot.command()
async def clearQueue(ctx):
    """Clears the queue for the music bot. Usage: clearQueue"""
    q[ctx.guild.id] = []