import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# get token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#variables
l_names = [] #list of names
d_names = {} #dictionary of names
bot = commands.Bot(command_prefix='#')

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

#@bot.command()
#async def schedule_daily_message():

bot.run(TOKEN)