from operator import index
import discord
import aiosqlite
from pathlib import Path
from builtins import bot
from tracemalloc import start
from discord.ext import tasks
from datetime import datetime , date, timedelta 
import scheduleFunctions

FORMATERROR = -1
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

@bot.command()
async def schedule(ctx, paramOne:str ,paramTwo:int, message:str, stringList:str = "", dateStart:str = ""):
    if type(paramTwo) != int:
         await ctx.reply("Unrecognized time frame")
    time = scheduleFunctions.convertToMinutes(paramOne,paramTwo)
    if time == FORMATERROR:
        await ctx.reply("Unrecognized. Please use m for minutes, h for hours, d for days instead of " + paramOne)
        return
    finalTime = scheduleFunctions.dateConversion(dateStart)
    if finalTime == FORMATERROR:
        await ctx.reply("Error in assigning time. Please use correct format (%Y-%m-%d, %H:%M) /a future time period")
        return 
    await ctx.reply(await scheduleFunctions.insertScheduler(ctx.guild.id,time,finalTime,paramOne,paramTwo,message,stringList))
    try:
        scheduledMessage.start(ctx)
    except:
        print("Already running scheduledMessage")

@bot.command()
async def continueSchedule(ctx):
    repeat = await scheduleFunctions.repeatUntilPresentFunction(ctx.guild.id)
    if repeat:
        scheduledMessage.start(ctx)
    else:
        await ctx.reply("No scheduled messages")


@bot.command()
async def stopSchedule(ctx):
    scheduledMessage.cancel()
    await ctx.reply("Stopped schedule(s)")

@bot.command()
async def deleteSchedule(ctx,id:int):
    await ctx.reply(await scheduleFunctions.deleteScheduleFunction(ctx.guild.id,id))

@bot.command()
async def clearSchedule(ctx):
    scheduledMessage.cancel()
    await ctx.reply(await scheduleFunctions.clearScheduleFunction(ctx.guild.id))

@bot.command()
async def getSchedule(ctx):
    await ctx.reply(await scheduleFunctions.getScheduleFunction(ctx.guild.id))
                 

@tasks.loop(minutes=1)
async def scheduledMessage(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if not data:
                scheduledMessage.cancel()
            else:
                for d in data:
                    d = list(d)
                    try:
                        expectedTime = datetime.strptime(d[2],DATEFORMAT)
                    except:
                        expectedTime = datetime.strptime(d[2],"%Y-%m-%d %H:%M:%S.%f")
                    currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
                    outcome = int((expectedTime-currentTime).total_seconds() / 60)
                    print(f"{d} and time diff is {outcome}")

                    await cursor.execute("SELECT list from restrictTable WHERE guild = ? AND category = ?",(ctx.guild.id,"schedule"))
                    c = await cursor.fetchone()
                    if c:
                        channel = discord.utils.get(ctx.guild.text_channels, name=c[0])
                    else:
                        channel = None
                    print(f"{channel} is the channel gotten")
                    if outcome<1:
                        if len(d[5]) == 0 and channel == None:
                            await ctx.send(f"scheduled message: {d[4]}")
                        elif len(d[5]) == 0 and channel:
                            await channel.send(f"scheduled message: {d[4]}")
                        else:
                            l = d[5].split(" ")
                            if channel!=None:
                                await channel.send(f"scheduled Message: {d[4]} {l[d[3]]}")
                            else:
                                await ctx.send(f"scheduled Message: {d[4]} {l[d[3]]}")
                            d[3] = (d[3]+1)%len(l)
                            await cursor.execute("UPDATE schedulesTable SET currentIndex = ? WHERE guild = ? AND id = ?",(d[3],ctx.guild.id,d[6]))
                        nextTime = datetime.now()+timedelta(minutes=d[1])
                        await cursor.execute("UPDATE schedulesTable SET alarmTime = ? WHERE guild = ? AND id = ?",(nextTime,ctx.guild.id,d[6]))
                    d = tuple(d)
        await db.commit()


