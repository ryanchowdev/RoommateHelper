import discord
from discord.ext import commands

#variables
l_names = [] #list of names
d_names = {} #dictionary of names
token = ''
bot = commands.Bot(command_prefix='#')

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

#@bot.command()
#async def schedule_daily_message():


#insert token into bot.run( discord bot token )

bot.run(token)