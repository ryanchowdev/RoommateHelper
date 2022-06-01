import os
from re import A
import discord
from discord.ext import commands
from dotenv import load_dotenv
from builtins import bot
import pollFunctions

EMPTY = 0
MAX_OPTIONS = 10

DEFAULT_VALID = 1
ERROR_NUM_VOTES_ZERO = -1
ERROR_OPTIONS_VOTE_MISMATCH = -2
ERROR_EXCEED_MAX_VOTES = -3

@bot.command()
async def poll(ctx, vote: int=None, message="", *options):
   """Creates a poll based on input. Displays help menu if no input. Usage: poll numOfVotes message listOfOptions """
   
   reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
   if vote == None:
      embed=pollFunctions.displayIntroPage()
      await ctx.send(embed=embed)
   else:
      pollValidFlag = pollFunctions.checkIfValid(vote, len(options))
      
      if pollValidFlag == ERROR_NUM_VOTES_ZERO:
         await ctx.send(':no_entry: Number of options must be greater than 0')
      elif pollValidFlag == ERROR_OPTIONS_VOTE_MISMATCH:
         await ctx.send(':no_entry: Number of options must be the same number as number of votes')
      elif pollValidFlag == ERROR_EXCEED_MAX_VOTES:
         await ctx.send(':no_entry: Number of votes must be less than or equal to 10')
      else:
         embed = pollFunctions.displayPoll(message, *options)
            
         msg = await ctx.channel.send(embed=embed)
         for i in range(vote):
            await msg.add_reaction(reactions[i])
   
