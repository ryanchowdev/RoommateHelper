import os
from re import A
import discord
from discord.ext import commands
from dotenv import load_dotenv
from builtins import bot

@bot.command()
async def poll(ctx,*,message):
   embed = discord.Embed(title=" POLL ", description = message)
   msg = await ctx.channel.send(embed=embed)
   await msg.add_reaction('1️⃣')
   await msg.add_reaction('2️⃣')
   
   # https://getemoji.com/