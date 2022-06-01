import os
import pickle
from pathlib import Path
from builtins import bot
from datetime import datetime , date 
from pytz import timezone
import pytz
import aiosqlite
import alarmFunctions

from discord.ext import tasks



@bot.command()
async def alarm(ctx, event:str,date:str, time:str):
  #check date/time input format
  try:
    date_format = datetime.strptime(date, '%m/%d/%Y')
    time_format = datetime.strptime(time, '%H:%M')
    await alarmFunctions.alarm(event, date, time, ctx.guild.id)
    await ctx.reply(f"Added alarm for {event} on {date} at {time}")
    if not check_time.is_running():
      check_time.start(ctx)
  except ValueError:
    await ctx.reply(f"Incorrect Format. Example usage: alarm event ")

@bot.command()
async def checkalarm(ctx): 
  await ctx.reply(await alarmFunctions.checkalarm(ctx.guild.id))

@bot.command()
async def clearalarm(ctx):
  await ctx.reply(await alarmFunctions.clearalarm(ctx.guild.id))

@bot.command()
async def removealarm(ctx, event:str):
  await ctx.reply(await alarmFunctions.removealarm(event,ctx.guild.id))    



#check for alarms and compare to current time once per minute
@tasks.loop(minutes=1.0, count=None)
async def check_time(ctx): 

  today = datetime.now().astimezone(timezone('US/Pacific'))
  today_time = today.strftime("%H:%M")
  #remove leading zeroes from dates for consistency
  today_date = "%d/%d/%d"%(today.month, today.day, today.year)
  async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from alarmsTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                for i in data:
                  event_date = datetime.strptime(i[2], '%m/%d/%Y')
                  event_date = "%d/%d/%d"%(event_date.month, event_date.day, event_date.year)
                  if i[2] <= today_date or (i[2] == today_date and i[3] <= today_time):
                    await ctx.reply(f"{i[1]} starting.")
                    await cursor.execute("DELETE FROM alarmsTable WHERE guild = ? AND event  = ?" ,(ctx.guild.id, i[1]))
                    await db.commit()
                    

