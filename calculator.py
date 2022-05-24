import math
from discord.ext import commands
import discord
import random
from builtins import bot
import ast
import parser
import inspect
import calcFunctions

VALID = 0
NOINPUT = -1
HASLETTERS = -2 

@bot.command()
async def calc(ctx,*,equation=""):
   checkInputFlag = calcFunctions.checkValidInput(equation)
   
   if checkInputFlag == VALID:
      res = calcFunctions.calculate(equation)
      if res == None:
         await ctx.send(":no_entry: Invalid input for equation")
      else:
         await ctx.send(res)
   elif checkInputFlag == NOINPUT:
      await ctx.send(":no_entry: Please enter an input")
   elif checkInputFlag == HASLETTERS:
      await ctx.send(":no_entry: Equations must contain only numbers and symbols")
