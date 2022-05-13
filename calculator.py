import math
from discord.ext import commands
import discord
import random
from builtins import bot
import ast
import parser
import inspect

@bot.command()
async def calc(ctx,*,equation=""):
   
   if equation == "":
      await ctx.send("Error: Please insert equation")
   else:
      #code = ast.parse(equation, "<string>", mode="eval")
      #await ctx.send(eval_node(code))
      if len(equation) == 0:
         await ctx.send("Error: Invalid Input for Equation")
      valid = True
      for i in equation:
         if (i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z'):
            valid = False
      
      if valid == True:   
         try:
            code = eval(equation)
            await ctx.send(code)
         except:
            await ctx.send("Error: Invalid Input for Equation")
      else:
         await ctx.send("Error: Invalid Input for Equation")
