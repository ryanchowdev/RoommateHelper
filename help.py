import os
from re import A
import discord
from discord.ext import commands
from dotenv import load_dotenv
from builtins import bot

'''
class Select(discord.ui.Select):
   def __init__(self):
      options=[
         discord.SelectOption(label="Option 1", description="Test 1"),
         discord.SelectOption(label="Option 2", description="Test 2"),
         discord.SelectOption(label="Option 3", description="Test 3")
      ]
      super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
      
class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())
        
@bot.command()
async def menu(ctx):
   await ctx.send("Menus!", view=Select())
'''      
switcher = {
   "": 1,
   "weather": 2,
   "money": 3,
   "schedule": 4,
   "alarm": 5,
   "calculator": 6
}

@bot.command()
async def helper(ctx,option=""):
   number = switcher.get(option)
   #await ctx.send(number)
   
   if number == 1: #default
      embed=discord.Embed(
         title="RoommateHelper : Help Menu ( = )", 
         description="",
         color=discord.Color.blue()
         )
      
      #embed.set_author(name="RoommateHelper : Help Menu")
      embed.add_field(
         name="**Weather**", 
         value="=helper weather", 
         inline=False
         )
      
      embed.add_field(
         name="**Money**", 
         value="=helper money", 
         inline=False
         )
      
      embed.add_field(
         name="**Schedule**", 
         value="=helper schedule", 
         inline=False
         )
      
      embed.add_field(
         name="**Alarm**", 
         value="=helper alarm", 
         inline=False
         )
      
      embed.add_field(
         name="**Calculator**", 
         value="=helper calculator", 
         inline=False
         )
      
   elif number == 2: #weather
      embed=discord.Embed(
         title="RoommateHelper : Weather ( = )", 
         description="",
         color=discord.Color.blue()
         )
      
      #embed.set_author(name="RoommateHelper : Weather")
      embed.add_field(
         name="**Command 1**", 
         value="=command1", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 2**", 
         value="=command2", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 3**", 
         value="=command3", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 4**", 
         value="=command4", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 5**", 
         value="=command5", 
         inline=False
         )
   elif number == 3: #money
      embed=discord.Embed(
         title="RoommateHelper : Money ( = )", 
         description="",
         color=discord.Color.blue()
         )
      
      #embed.set_author(name="RoommateHelper : Money")
      embed.add_field(
         name="**Command 1**", 
         value="=command1", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 2**", 
         value="=command2", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 3**", 
         value="=command3", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 4**", 
         value="=command4", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 5**", 
         value="=command5", 
         inline=False
         )
   elif number == 4: #schedule
      embed=discord.Embed(
         title="RoommateHelper : Schedule ( = )", 
         description="",
         color=discord.Color.blue()
         )
      
      #embed.set_author(name="RoommateHelper : Schedule")
      embed.add_field(
         name="**Command 1**", 
         value="=command1", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 2**", 
         value="=command2", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 3**", 
         value="=command3", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 4**", 
         value="=command4", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 5**", 
         value="=command5", 
         inline=False
         )
   elif number == 5: #alarm
      embed=discord.Embed(
         title="RoommateHelper : Alarm ( = )", 
         description="",
         color=discord.Color.blue()
         )
      
      #embed.set_author(name="RoommateHelper : Alarm")
      embed.add_field(
         name="**Command 1**", 
         value="=command1", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 2**", 
         value="=command2", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 3**", 
         value="=command3", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 4**", 
         value="=command4", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 5**", 
         value="=command5", 
         inline=False
         )
   elif number == 6: #calculator
      embed=discord.Embed(
         title="RoommateHelper : Calculator ( = )", 
         description="",
         color=discord.Color.blue()
         )
      
      #embed.set_author(name="RoommateHelper : Help Menu")
      embed.add_field(
         name="**Command 1**", 
         value="=command1", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 2**", 
         value="=command2", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 3**", 
         value="=command3", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 4**", 
         value="=command4", 
         inline=False
         )
      
      embed.add_field(
         name="**Command 5**", 
         value="=command5", 
         inline=False
         )
   
   await ctx.send(embed=embed)