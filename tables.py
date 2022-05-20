import os
import aiosqlite
from pathlib import Path
from builtins import bot
 
DBFILE = "main.db"

# Create tables in here
async def create_tables():
    try:
        aiosqlite.connect(DBFILE)
    except:
        print(f"Error with {DBFILE}")
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS rulesTable (guild INTEGER, rules TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS schedulesTable (guild INTEGER, timeBetween INTEGER, alarmTime DATETIME,currentIndex INTEGER,message TEXT,list TEXT, id INTEGER)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS alarmsTable (guild INTEGER, event TEXT, date TEXT, time TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS restrictTable (guild INTEGER, category TEXT,list TEXT)')
            await cursor.execute('CREATE TABLE IF NOT EXISTS moneyTable (guild INTEGER, person TEXT, amount REAL)')
        await db.commit()
