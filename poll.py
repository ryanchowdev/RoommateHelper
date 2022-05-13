import os
from re import A
import discord
from discord.ext import commands
from dotenv import load_dotenv
from builtins import bot

@bot.command()
async def poll(ctx, vote: int=None, message="", *options):
   
   reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
   if vote == None:
      embed=discord.Embed(
      title="RoommateHelper : Polls", 
      description="",
      color=discord.Color.blue()
      )
   
   #embed.set_author(name="RoommateHelper : Help Menu")
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
      await ctx.send(embed=embed)
   elif vote<=0:
         await ctx.send(':no_entry: Number of options must be greater than 0')
   elif len(options) != vote:
      await ctx.send(':no_entry: Number of options must be the same number as number of votes')
   elif len(options) > 10:
      await ctx.send(':no_entry: Number of votes must be less than or equal to 10')
   else:
         
      embed = discord.Embed(title="RoommateHelper : Polls", description = message)
      
      for i in range(len(options)):
         index = i + 1
         embed.add_field(
            name=options[i], 
            value=index, 
            inline=False
            )
         
      msg = await ctx.channel.send(embed=embed)
      for i in range(vote):
         await msg.add_reaction(reactions[i])
   
   # https://getemoji.com/
   
