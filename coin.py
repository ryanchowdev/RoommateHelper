import math
from discord.ext import commands
import discord
import random
from builtins import bot
   
@bot.command()
async def flip(ctx):
   res = random.randint(0,1)
   if res == 0:
       await ctx.reply("Heads")
   else:
      await ctx.reply("Tails")
   
