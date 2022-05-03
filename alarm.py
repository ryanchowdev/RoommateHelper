import os
import pickle
from pathlib import Path
from builtins import bot
from datetime import datetime , date 
from pytz import timezone
import pytz
import aiosqlite


from discord.ext import tasks



@bot.command()
async def alarm(ctx, event:str,date:str, time:str):
  #check date/time input format
  try:
    date_format = datetime.strptime(date, '%m/%d/%Y')
    time_format = datetime.strptime(time, '%H:%M')
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from alarmsTable WHERE guild = ? AND event = ? AND date = ? AND time = ?",(ctx.guild.id,event,date, time))
            data = await cursor.fetchone()
            if data:
                await ctx.reply("Already scheduled. ")
                return
            else:
                await cursor.execute("INSERT INTO alarmsTable (guild,event,date,time) VALUES (?,?,?,?)",(ctx.guild.id,event,date,time))
            await ctx.reply(f"Added alarm for {event} on {date} at {time}")
            await db.commit()    
    if not check_time.is_running():
      check_time.start(ctx)
  except ValueError:
    await ctx.reply(f"Incorrect Format. Example usage: alarm event 7/22/2019 15:00")

@bot.command()
async def checkalarm(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from alarmsTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                string = "Current Alarms\n"
                for i in data:
                    string += f"{(i[1])} {(i[2])}  {i[3]}  \n"
                await ctx.reply(string)
            else:
                await ctx.reply(" NO ALARMS CURRENTLY")

@bot.command()
async def clearalarm(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM alarmsTable WHERE guild = ?",(ctx.guild.id,))
        await ctx.reply("DELETED ALARMS")
        await db.commit()

@bot.command()
async def removealarm(ctx, event:str):
    found = False
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from alarmsTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                for i in data:
                    if(i[1] == event):
                      found = True
                      await cursor.execute("DELETE FROM alarmsTable WHERE guild = ? AND event  = ?" ,(ctx.guild.id, i[1]))
                      await ctx.reply(f"Removed alarm - {event}.")    
                      await db.commit()
    if(found == False):
      await ctx.reply(f"Alarm does not exist.")    



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
                  if i[2] <= today_date and i[3] <= today_time:
                    await ctx.reply(f"{i[1]} starting.")
                    await cursor.execute("DELETE FROM alarmsTable WHERE guild = ? AND event  = ?" ,(ctx.guild.id, i[1]))
                    await db.commit()
                    

