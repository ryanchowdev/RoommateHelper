import os
import string
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import builtins

# get token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#variables
l_names = [] #list of names
d_names = {} #dictionary of names
bot = commands.Bot(command_prefix='=')

builtins.bot = bot

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

@bot.command()
async def schedule(ctx, paramOne:str = "m" ,paramTwo:int = 1,message:str = "MSG"):
    if type(paramTwo) != int:
         await ctx.reply("Unrecognized time frame")

    time = paramTwo
    if paramOne in ["m","minute","min"]:
        paramOne = "minute"
    elif paramOne in ["h","hour"]:
        paramOne = "hour"
        time*=60
    elif paramOne in ["d","day"]:
        paramOne = "day"
        time*=60*24
    else:
        await ctx.reply("Unrecognized please use m for minutes, h for hours, d for days instead of " + paramOne)
    await ctx.reply("Scheduled a message every "+ str(paramTwo)+" "+paramOne)
    scheduledMessage.change_interval(minutes = int(time))
    scheduledMessage.start(ctx,message)

@bot.command()
async def stop(ctx):
    scheduledMessage.cancel()
    await ctx.reply("Stopped message")

@tasks.loop(minutes=1)
async def scheduledMessage(ctx,message):
    await ctx.send(message)

# import bot features
import weather
import money

bot.run(TOKEN)