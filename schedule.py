from operator import index
import os
import random
from random import randint
import aiosqlite
from pathlib import Path
from builtins import bot
from tracemalloc import start
from discord.ext import tasks
from datetime import datetime , date 

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
    else:
        await ctx.reply("Unrecognized. Please use m for minutes, h for hours, d for days instead of " + paramOne)
        return
    timeBetween = time
    if dateStart !="":
        try:
            date_format = datetime.strptime(dateStart, "%m/%d/%Y %H:%M")
            print(f"date format is {date_format}")
            diff = date_format-datetime.now() 
            diff = int(diff.total_seconds() / 60)
            print(f"diff is {diff}")
            if diff <0:
                await ctx.reply("Time has already passed. Please reschedule")
                return
            timeBetween+= abs(diff)
        except:
            print(f"exception: dateStart is {dateStart}")
            await ctx.reply("Unrecognized time format. Needs both date m/d/y and h:m in one string for start time")
            return
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
            await cursor.execute("INSERT INTO schedulesTable (guild,timeBetween,timeLeft,message,list,currentIndex,id) VALUES (?,?,?,?,?,?,?)",(ctx.guild.id,time,timeBetween+1,message,stringList,0,code))
            await ctx.reply("Scheduled a message every "+ str(paramTwo)+" "+paramOne+" Message: " + message)
            await db.commit()
    scheduledMessage.start(ctx)

@bot.command()
async def continueSchedule(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
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
                    string += f"{(i[4])} in {i[2]} minute(s) id is {i[6]}\n"
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
                    print(d)
                    d = list(d)
                    d[2]-=1
                    await cursor.execute("UPDATE schedulesTable SET timeLeft = ? WHERE guild = ? AND message = ? AND timeBetween = ? AND list = ?",(d[2],ctx.guild.id,d[4],d[1],d[5]))
                    if d[2]<=0:
                        if len(d[5]) == 0:
                            await ctx.send(f"scheduled message: {d[4]}")
                        else:
                            l = d[5].split(" ")
                            await ctx.send(f"scheduled Message: {d[4]} {l[d[3]]}")
                            d[3] = (d[3]+1)%len(l)
                            await cursor.execute("UPDATE schedulesTable SET currentIndex = ? WHERE guild = ? AND message = ? AND timeBetween = ? AND list = ?",(d[3],ctx.guild.id,d[4],d[1],d[5]))
                        await cursor.execute("UPDATE schedulesTable SET timeLeft = ? WHERE guild = ? AND message = ? AND timeBetween = ? AND list = ?",(d[1],ctx.guild.id,d[4],d[1],d[5]))
                    d = tuple(d)
        await db.commit()