import os
import pickle
from pathlib import Path
from builtins import bot
import string
from tracemalloc import start
from discord.ext import tasks

#dictionary to store indexs of lists relative to stuff
d = {}

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
async def schedule(ctx, paramOne:str ,paramTwo:int, message:str, stringList:str = ""):
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

    l = stringList.split(" ")
    for i in l:
        print(i)
    messageCode = paramOne+str(time)+message[0]+str(len(l))
    if Path('schedule.pkl').is_file() and os.stat('schedule.pkl').st_size != 0:
        schedule = load_from_fileSchedule('schedule.pkl')
        for key in schedule:
            d[key]=0
            if schedule[key] == [paramOne,time,message,time,l]:
                await ctx.reply("Already scheduled please resume or delete instead")
                return
    record_schedule(messageCode,[paramOne,time,message,time,l])
    d[messageCode]=0
    await ctx.reply("Scheduled a message every "+ str(paramTwo)+" "+paramOne+" code is " + messageCode)
    try:
        scheduledMessage.start(ctx)
    except:
        pass

@bot.command()
async def continueSchedule(ctx):
    try:
        if os.stat('schedule.pkl').st_size != 0:
            scheduledMessage.start(ctx)
    except:
        await ctx.reply("No current Schedules")


#@bot.command()
#async def startSchedule(ctx):
#    try:
#        await ctx.send("Starting Schedule")
#        scheduledMessage.start(ctx)
#    except:
#        await ctx.send("could not start schedule")

@bot.command()
async def stopSchedule(ctx):
    scheduledMessage.cancel()
    await ctx.reply("Stopped schedule(s)")

@bot.command()
async def clearSchedule(ctx):
    scheduledMessage.cancel()
    open("schedule.pkl", "w").close()
    d.clear()
    await ctx.reply(f"All schedules cleared.")

@bot.command()
async def currentSchedule(ctx):
    try:
        if os.stat('schedule.pkl').st_size != 0:
            schedule = load_from_fileSchedule('schedule.pkl')
            await ctx.reply("Current schedules:")
            for key in schedule:
                await ctx.reply(f"code: {key} msg: {schedule[key][2]}")
    except:
        await ctx.reply("Nothing currently scheduled")
                 

@tasks.loop(minutes=1)
async def scheduledMessage(ctx):
    if os.stat('schedule.pkl').st_size != 0:
        schedule = load_from_fileSchedule('schedule.pkl')
        for key in schedule:
            temp = schedule[key]
            temp[3] -= 1
            if temp[3] <=0:
                if len(temp[4]) == 0:
                    await ctx.send(f"scheduled message: {temp[2]}")
                else:
                    l = temp[4]
                    await ctx.send(f"scheduled message: {temp[2]} {l[d[key]]}")
                    d[key] = (d[key]+1)%len(temp[4])
                temp[3] = temp[1]