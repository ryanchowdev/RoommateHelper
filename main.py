import os
from re import A
import discord
from discord.ext import commands
from dotenv import load_dotenv

# get token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#variables
l_names = [] #list of names
d_names = {} #dictionary of names
bot = commands.Bot(command_prefix='=')

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

@bot.command()
async def helper(ctx):
   embed=discord.Embed(
      title="RoommateHelper : Help Menu ( = )", 
      description="",
      color=discord.Color.blue()
      )
   
   #embed.set_author(name="RoommateHelper : Help Menu")
   embed.add_field(
      name="**command1**", 
      value="Show description of command 1.", 
      inline=False
      )
   
   embed.add_field(
      name="**command2**", 
      value="Show description of command 2.", 
      inline=False
      )
   
   embed.add_field(
      name="**command3**", 
      value="Show description of command 3.", 
      inline=False
      )
   
   embed.add_field(
      name="**command4**", 
      value="Show description of command 4.", 
      inline=False
      )
   
   embed.add_field(
      name="**command5**", 
      value="Show description of command 5.", 
      inline=False
      )
   
   await ctx.send(embed=embed)

bot.run(TOKEN)