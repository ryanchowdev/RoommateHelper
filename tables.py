import os
import aiosqlite
from pathlib import Path
from builtins import bot
 
#Create tables in here
@bot.event
async def on_ready():
    print("CREATING TABLES NOW \n")
    try:
        aiosqlite.connect("main.db")
    except:
        print("Error with main.db")
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS rulesTable (guild INTEGER, rules TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS schedulesTable (guild INTEGER, timeBetween INTEGER, alarmTime DATETIME,currentIndex INTEGER,message TEXT,list TEXT, id INTEGER)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS alarmsTable (guild INTEGER, event TEXT, date TEXT, time TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS restrictTable (guild INTEGER, category TEXT,list TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS moneyTable (guild INTEGER, person TEXT, amount INTEGER)')
        await db.commit()
