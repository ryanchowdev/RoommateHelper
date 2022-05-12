import math
from discord.ext import commands
import discord
import random
from builtins import bot
   
@bot.command()
async def flip(ctx):
   res = random.randint(0,1)
   
   embed=discord.Embed(
         title="RoommateHelper : Coin Flip", 
         description="",
         color=discord.Color.blue()
      )
   
   if res == 0:
      embed.add_field(
         name="You got:", 
         value="Heads", 
         inline=False
      )
      embed.set_image(url="https://i.imgur.com/DsLFwRO.png")
   else:
      embed.add_field(
         name="You got:", 
         value="Tails", 
         inline=False
      )
      embed.set_image(url="https://i.imgur.com/3Xqr7Eh.png")
   
   await ctx.send(embed=embed)
