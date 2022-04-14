import os
import pickle
from pathlib import Path
from builtins import bot
from discord.ext import tasks

# Code below take from money.py (Ryan's code I believe)
def save_to_fileSchedule(dict, f):
    schedule_file = open(f, 'bw+')
    pickle.dump(dict, schedule_file)
    schedule_file.close()

def load_from_fileSchedule(f):
    # create pickle file if it does not exist
    myfile = Path(f)
    myfile.touch(exist_ok=True)
    # load
    schedule_file = open(myfile, 'br')
    schedule = pickle.load(schedule_file)
    schedule_file.close()
    return schedule

def record_schedule(name, amt):
    # create pickle file if it does not exist
    myfile = Path('schedule.pkl')
    myfile.touch(exist_ok=True)
    # only load from pickle file if it is nonempty
    schedule = load_from_fileSchedule('schedule.pkl') if os.stat('schedule.pkl').st_size != 0 else {}
    schedule.update({name: amt})
    save_to_fileSchedule(schedule, 'schedule.pkl')

@bot.command()
async def schedule(ctx, paramOne:str = "m" ,paramTwo:int = 1,message:str = "MSG"):
    if type(paramTwo) != int:
         await ctx.reply("Unrecognized time frame")
    time = paramTwo
    if paramOne in ["m","minute","min"]:
        paramOne = "minute"
    elif paramOne in ["h","hour"]:
        paramOne = "hour"
        time*=60
    elif paramOne in ["d","day"]:
        paramOne = "day"
        time*=60*24
    else:
        await ctx.reply("Unrecognized please use m for minutes, h for hours, d for days instead of " + paramOne)
        return
    if os.stat('schedule.pkl').st_size != 0:
        schedule = load_from_fileSchedule('schedule.pkl')
        for key in schedule:
            if message == key and schedule[key] == (paramOne,paramTwo):
                await ctx.reply("Already scheduled please resume or delete instead")
                return
    record_schedule(message,(paramOne,paramTwo))
    scheduledMessage.change_interval(minutes = int(time))
    scheduledMessage.start(ctx,message)
    await ctx.reply("Scheduled a message every "+ str(paramTwo)+" "+paramOne)

@bot.command()
async def stopSchedule(ctx):
    scheduledMessage.cancel()
    await ctx.reply("Stopped message")

@bot.command()
async def continueSchedule(ctx):
    if os.stat('schedule.pkl').st_size != 0:
        schedule = load_from_fileSchedule('schedule.pkl')
        for key in schedule:
            scheduledMessage.change_interval(minutes = int(schedule[key][1]))
            scheduledMessage.start(ctx,key)
            await ctx.reply(f"Continuing schedule for {key}")

#Not working right now
@bot.command()
async def deleteSchedule(ctx,message:str):
    if os.stat('schedule.pkl').st_size != 0:
        schedule = load_from_fileSchedule('schedule.pkl')
        try:
            del schedule[message]
            await ctx.reply(f"Deleted {message} {schedule[message][0]} {schedule[message][1]} from schedule")
        except:
            await ctx.reply(f"Failed to delete {message}")
    

@tasks.loop(minutes=1)
async def scheduledMessage(ctx,message):
    await ctx.send(message)