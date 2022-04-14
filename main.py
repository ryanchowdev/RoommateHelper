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
bot = commands.Bot(command_prefix='=')

builtins.bot = bot

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

# import bot features
import weather
import money
import schedule

bot.run(TOKEN)