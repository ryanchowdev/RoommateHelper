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
            await cursor.execute('CREATE TABLE IF NOT EXISTS rulesTable (guild INTEGER, rules STRING)')
        await db.commit()