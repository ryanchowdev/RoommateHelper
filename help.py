import os
from re import A
import discord
from discord.ext import commands
from dotenv import load_dotenv
from builtins import bot
import helpFunctions

DEFAULT = 1
ALARM = 2
CALCULATOR = 3
COINFLIP = 4
GMAPS = 5
MONEY = 6
MUSIC = 7
POLL = 8
RESTRICT = 9
RULES = 10
SCHEDULE = 11
WEATHER = 12
LISTS = 13

switcher = {
   "": DEFAULT,
   "alarm": ALARM,
   "calculator": CALCULATOR,
   "coinflip": COINFLIP,
   "gmaps": GMAPS,
   "money": MONEY,
   "music": MUSIC,
   "polls": POLL,
   "restrict": RESTRICT,
   "rules": RULES,
   "schedule": SCHEDULE,
   "weather": WEATHER,
   "lists": LISTS
}

@bot.command()
async def help(ctx,option=""):
   """Displays various help menus and commands. Usage: help <option (optional)>"""
   number = switcher.get(option)
   
   if number == DEFAULT:
      embed=helpFunctions.displayIntroPage()
   elif number == ALARM:
      embed=helpFunctions.displayAlarmPage()
   elif number == CALCULATOR:
      embed=helpFunctions.displayCalculatorPage()
   elif number == COINFLIP:
      embed=helpFunctions.displayCoinFlipPage()
   elif number == GMAPS:
      embed=helpFunctions.displayGMapsPage()
   elif number == MONEY:
      embed=helpFunctions.displayMoneyPage()
   elif number == MUSIC:
      embed=helpFunctions.displayMusicPage()
   elif number == POLL:
      embed=helpFunctions.displayPollPage()
   elif number == RESTRICT:
      embed=helpFunctions.displayRestrictPage()
   elif number == RULES:
      embed=helpFunctions.displayRulesPage()
   elif number == SCHEDULE:
      embed=helpFunctions.displaySchedulePage()
   elif number == WEATHER:
      embed=helpFunctions.displayWeatherPage()
   elif number == LISTS:
      embed=helpFunctions.displayListsPage()
      
   await ctx.send(embed=embed)