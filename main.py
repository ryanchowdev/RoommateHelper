import os
import string
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import builtins

# get token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#bot = discord.Client(intents=discord.Intents.default())
#variables
#bot = commands.Bot(command_prefix='=', intents=discord.Intents.all())
PREFIX = '='
bot = commands.Bot(command_prefix=PREFIX)

builtins.bot = bot

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

# import bot features
import weather
import money
import schedule
import alarm
import help
import calculator
import coin
import poll

bot.run(TOKEN)