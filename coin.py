import math
from discord.ext import commands
import discord
import random
from builtins import bot
import coinFunctions
   
HEADS = 0
TAILS = 1

@bot.command()
async def flip(ctx):
   """Flips a coin and randomly chooses between heads or tails. Usage: flip"""
   res = random.randint(HEADS,TAILS)
   
   if res == HEADS:
      embed=coinFunctions.displayHeads()
   else:
      embed=coinFunctions.displayTails()
   
   await ctx.send(embed=embed)
