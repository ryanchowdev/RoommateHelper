import os
import pickle
from pathlib import Path
from builtins import bot
from datetime import datetime
from datetime import date

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
  try:
    date_format = datetime.strptime(date, '%m/%d/%Y')
    time_format = datetime.strptime(time, '%H:%M')
    record_alarm(event, (date, time))
    await ctx.reply(f"Added alarm for {event} on {date} at {time}")
  except ValueError:
    await ctx.reply(f"Incorrect Format. Example usage: alarm event 7/22/2019 15:00")

@bot.command()
async def checkalarm(ctx):
    if os.stat('alarms.pkl').st_size != 0:
        message = ""
        alarms = load_from_file_Alarm('alarms.pkl')
        for event in alarms:
            message += f"{event}, {alarms[event][0]}, {alarms[event][1]} \n"
        await ctx.reply(f"Current alarms:\n{message}")
    else:
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

