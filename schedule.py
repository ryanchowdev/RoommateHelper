from operator import index
import os
import random
from random import randint
import aiosqlite
from pathlib import Path
from builtins import bot
from tracemalloc import start
from discord.ext import tasks
from datetime import datetime , date, timedelta 

dateFormat = "%Y-%m-%d %H:%M:%S"

@bot.command()
async def schedule(ctx, paramOne:str ,paramTwo:int, message:str, stringList:str = "", dateStart:str = ""):
    #Make sure parameters are good/convert time to minutes
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
    elif paramOne in ["week","w"]:
        paramOne = "week"
        time*=60*24*7
    elif paramOne in ["year","y"]:
        paramOne = "year"
        time*=60*24*365
    else:
        await ctx.reply("Unrecognized. Please use m for minutes, h for hours, d for days instead of " + paramOne)
        return
    currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
    if dateStart !="":
        try:
            currentTime = datetime.strptime(dateStart, "%m/%d/%Y %H:%M")
        except:
            print(f"exception: dateStart is {dateStart}")
            await ctx.reply("Unrecognized time format. Needs both date m/d/y and h:m in one string for start time")
            return
    finalTime = currentTime
    #Check if already exists
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            code = random.randint(100000000,999999999)
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ? AND id = ?",(ctx.guild.id,code))
            data = await cursor.fetchone()
            while data:
                code = random.randint(100000000,999999999)
                await cursor.execute("SELECT * from schedulesTable WHERE guild = ? AND id = ?",(ctx.guild.id,code))
                data = await cursor.fetchone()
            await cursor.execute("INSERT INTO schedulesTable (guild,timeBetween,alarmTime,message,list,currentIndex,id) VALUES (?,?,?,?,?,?,?)",(ctx.guild.id,time,finalTime,message,stringList,0,code))
            await ctx.reply("Scheduled a message every "+ str(paramTwo)+" "+paramOne+" Message: " + message)
            await db.commit()
    try:
        scheduledMessage.start(ctx)
    except:
        print("Already running scheduledMessage")

@bot.command()
async def continueSchedule(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                data = await cursor.fetchall()
                currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
                for d in data:
                    d = list(d)
                    expectedTime = datetime.strptime(d[2],dateFormat)
                    while int((expectedTime-currentTime).total_seconds() / 60)<=0:
                        expectedTime = currentTime+timedelta(minutes=d[1])
                    d[2] = expectedTime
                    d = tuple(d)
                scheduledMessage.start(ctx)
            else:
                await ctx.reply("No scheduled messages")


@bot.command()
async def stopSchedule(ctx):
    scheduledMessage.cancel()
    await ctx.reply("Stopped schedule(s)")

@bot.command()
async def deleteSchedule(ctx,id:int):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM schedulesTable WHERE guild = ? AND id = ?",(ctx.guild.id,id))
        await ctx.reply("DELETED SCHEDULE")
        await db.commit()

@bot.command()
async def clearSchedule(ctx):
    scheduledMessage.cancel()
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM schedulesTable WHERE guild = ?",(ctx.guild.id,))
        await ctx.reply("DELETED SCHEDULES")
        await db.commit()

@bot.command()
async def getSchedule(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                string = "SCHEDULES\n"
                for i in data:
                    print(i)
                    string += f"{(i[4])} at {i[2]} id is {i[6]}\n"
                await ctx.reply(string)
            else:
                await ctx.reply(" NO Schedules CURRENTLY")
                 

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
                    expectedTime = datetime.strptime(d[2],dateFormat)
                    currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
                    outcome = int((expectedTime-currentTime).total_seconds() / 60)
                    print(f"{d} and time diff is {outcome}")
                    if outcome<1:
                        if len(d[5]) == 0:
                            await ctx.send(f"scheduled message: {d[4]}")
                        else:
                            l = d[5].split(" ")
                            await ctx.send(f"scheduled Message: {d[4]} {l[d[3]]}")
                            d[3] = (d[3]+1)%len(l)
                            await cursor.execute("UPDATE schedulesTable SET currentIndex = ? WHERE guild = ? AND id = ?",(d[3],ctx.guild.id,d[6]))
                        nextTime = datetime.now()+timedelta(minutes=d[1])
                        await cursor.execute("UPDATE schedulesTable SET alarmTime = ? WHERE guild = ? AND id = ?",(nextTime,ctx.guild.id,d[6]))
                    d = tuple(d)
        await db.commit()


