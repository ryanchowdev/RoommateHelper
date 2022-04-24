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
PREFIX = '='
bot = commands.Bot(command_prefix=PREFIX)
builtins.bot = bot

@bot.event
async def on_ready():
    # Set help message in status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}help"))

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
import rules
import tables

bot.run(TOKEN)