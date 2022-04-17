import os
import pickle
from pathlib import Path
from builtins import bot
from datetime import datetime , date 
from pytz import timezone
import pytz

from discord.ext import tasks

def save_to_file_Alarm(dict, f):
    alarms_file = open(f, 'bw+')
    pickle.dump(dict, alarms_file)
    alarms_file.close()

def load_from_file_Alarm(f):
    # create pickle file if it does not exist
    myfile = Path(f)
    myfile.touch(exist_ok=True)
    # load
    alarms_file = open(myfile, 'br')
    alarms = pickle.load(alarms_file)
    alarms_file.close()
    return alarms

def record_alarm(event, time):
    # create pickle file if it does not exist
    myfile = Path('alarms.pkl')
    myfile.touch(exist_ok=True)
    # only load from pickle file if it is nonempty
    alarms = load_from_file_Alarm('alarms.pkl') if os.stat('alarms.pkl').st_size != 0 else {}
    alarms.update({event: time})
    save_to_file_Alarm(alarms, 'alarms.pkl')

@bot.command()
async def alarm(ctx, event:str,date:str, time:str):
  #check date/time input format
  try:
    date_format = datetime.strptime(date, '%m/%d/%Y')
    time_format = datetime.strptime(time, '%H:%M')
    record_alarm(event, (date, time))
    await ctx.reply(f"Added alarm for {event} on {date} at {time}")
    if not check_time.is_running():
      check_time.start(ctx)
  except ValueError:
    await ctx.reply(f"Incorrect Format. Example usage: alarm event 7/22/2019 15:00")

@bot.command()
async def checkalarm(ctx):
  #check if alarm pickle file exists
  try:
    if os.stat('alarms.pkl').st_size != 0:
        message = ""
        alarms = load_from_file_Alarm('alarms.pkl')
        for event in alarms:
            message += f"{event}, {alarms[event][0]}, {alarms[event][1]} \n"
        await ctx.reply(f"Current alarms:\n{message}")
    else:
        await ctx.reply(f"No current alarms.")
  except:
    await ctx.reply(f"No current alarms.")

@bot.command()
async def clearalarm(ctx):
    open("alarms.pkl", "w").close()
    await ctx.reply(f"All alarms cleared.")

@bot.command()
async def removealarm(ctx, event:str):
  alarms = load_from_file_Alarm('alarms.pkl')
  if event not in alarms:
    await ctx.reply(f"Alarm does not exist.")    
  else:  
    del(alarms[event])
    alarms.update()
    save_to_file_Alarm(alarms, 'alarms.pkl')
    await ctx.reply(f"Removed alarm - {event}.")    

#check for alarms and compare to current time once per minute
#will make this more efficient in later
@tasks.loop(minutes=1.0, count=None)
async def check_time(ctx): 
  alarms = load_from_file_Alarm('alarms.pkl')
  alarms_copy = {}
  today = datetime.now().astimezone(timezone('US/Pacific'))
  today_time = today.strftime("%H:%M")
  #remove leading zeroes from dates for consistency
  today_date = "%d/%d/%d"%(today.month, today.day, today.year)
  removed = False
  for event in alarms:
    event_date = datetime.strptime(alarms[event][0], '%m/%d/%Y')
    event_date = "%d/%d/%d"%(event_date.month, event_date.day, event_date.year)
    #removing finished alarms from list
    if alarms[event][0] <= today_date and alarms[event][1] <= today_time:
      removed = True
      await ctx.reply(f"{event} starting.") 
    else:
      alarms_copy[event] = alarms[event]
      alarms_copy.update()
      save_to_file_Alarm(alarms_copy, 'alarms.pkl')
  if removed == True and len(alarms) == 1:
    open("alarms.pkl", "w").close()
    #stop checking when no alarms left
    check_time.cancel()