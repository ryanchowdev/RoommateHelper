import math
from discord.ext import commands
import discord
import random
from builtins import bot

@bot.command()
async def add(ctx, x: float, y: float):
   res = x + y
   await ctx.send(res)
   
@bot.command()
async def sub(ctx, x: float, y: float):
   res = x - y
   await ctx.send(res)
   
@bot.command()
async def mul(ctx, x: float, y: float):
   res = x * y
   await ctx.send(res)
   
@bot.command()
async def div(ctx, x: float, y: float):
   res = x / y
   await ctx.send(res)
   
@bot.command()
async def sqrt(ctx, x: float):
   res = math.sqrt(x)
   await ctx.send(res)
   
@bot.command()
async def rand(ctx, x: int, y: int):
   res = random.randint(x,y)
   await ctx.send(res)
