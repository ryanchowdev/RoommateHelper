import os
from re import A
import discord
from discord.ext import commands
import youtube_dl 
from builtins import bot

#Using https://www.youtube.com/watch?v=jHZlvRr9KxM&t=167s as basis
#Also https://github.com/afazio1/robotic-nation-proj/blob/master/projects/discord-bot/voice.py


@bot.command()
async def musicJoin(ctx):
    if ctx.author.voice is None:
       await ctx.send("Join a voice channel before asking me to join")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    
@bot.command()
async def musicLeave(ctx):
    await ctx.voice_client.disconnect()
    
@bot.command()
async def playMusic(ctx,url):
    if ctx.author.voice is None:
       await ctx.send("Join a voice channel before asking me to join")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    try:
        ctx.voice_client.stop()
    except:
        print("Nothign running")
    FMMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url,download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2,**FMMPEG_OPTIONS)
        vc.play(source)

@bot.command()
async def musicPause(ctx):
    try:
        await ctx.voice_client.pause()
    except:
        print("caught exception in musicPause")
    await ctx.send("Paused Music")

@bot.command()
async def musicResume(ctx):
    try:
        await ctx.voice_client.resume()
    except:
        print("caught exception in musicResume")
    await ctx.send("Resumed Music")
        



