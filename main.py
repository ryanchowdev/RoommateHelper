import os
from re import A
import discord
from discord.ext import commands
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

import help

bot.run(TOKEN)