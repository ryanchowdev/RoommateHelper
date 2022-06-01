import os
from re import A
import discord
from discord.ext import commands

EMPTY = 0
MAX_OPTIONS = 10

DEFAULT_VALID = 1
ERROR_NUM_VOTES_ZERO = -1
ERROR_OPTIONS_VOTE_MISMATCH = -2
ERROR_EXCEED_MAX_VOTES = -3

def displayIntroPage():
    embed=discord.Embed(
      title="RoommateHelper : Polls", 
      description="",
      color=discord.Color.blue()
      )
    embed.add_field(
        name="**Command Format**", 
        value="=poll numOfVotes message listOfOptions", 
        inline=False
        )
    
    embed.add_field(
        name="**Example**", 
        value="=poll 3 \"When should we eat?\" Breakfast Lunch \"Dinner Time\"\n\n This will give a poll with three options: Breakfast, Lunch, and Dinner Time", 
        inline=False
        )
    
    embed.add_field(
        name="**Note**", 
        value="Number of votes must match number of options. For multi-worded options, use quotations.", 
        inline=False
        )
    return embed
    
def checkIfValid(vote, pollLength):
    pollValidFlag = DEFAULT_VALID
    
    if vote<=EMPTY:
        pollValidFlag = ERROR_NUM_VOTES_ZERO
    elif pollLength != vote:
        pollValidFlag = ERROR_OPTIONS_VOTE_MISMATCH
    elif pollLength > MAX_OPTIONS:
        pollValidFlag = ERROR_EXCEED_MAX_VOTES
        
    return pollValidFlag

def displayPoll(message, *options):
    embed = discord.Embed(title="RoommateHelper : Polls", description = message)
         
    for i in range(len(options)):
        index = i + 1
        embed.add_field(
            name=options[i], 
            value=index, 
            inline=False
            )
        
    return embed