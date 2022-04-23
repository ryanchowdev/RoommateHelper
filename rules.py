import os
from pathlib import Path
from builtins import bot
import aiosqlite

# CREATE Rules Table
@bot.event
async def on_ready():
    print("Bot is now running")
    try:
        aiosqlite.connect("rules.db")
    except:
        print("Error with rules.db")
    async with aiosqlite.connect("rules.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS users (guild INTEGER, rules STRING)')
        await db.commit()
        

@bot.command()
async def addRule(ctx, *args):
    rule = ""
    for i in args:
        rule += f"{i} "
    async with aiosqlite.connect("rules.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT rules from users WHERE guild = ? AND rules = ?",(ctx.guild.id,rule))
            data = await cursor.fetchone()
            if data:
                await ctx.reply(f"Rule already exists: {rule}")
            else:
                await cursor.execute("INSERT INTO USERS (rules,guild) VALUES (?,?)",(rule,ctx.guild.id))
                await ctx.reply(f"Rule added: {rule}")
        await db.commit()

@bot.command()
async def getRules(ctx):
    async with aiosqlite.connect("rules.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT rules from users WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                string = "RULES\n"
                for i in data:
                    string += f"{(i[0])} \n"
                await ctx.reply(string)
            else:
                await ctx.reply(" NO RULES CURRENTLY")

@bot.command()
async def clearRules(ctx):
    async with aiosqlite.connect("rules.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM users WHERE guild = ?",(ctx.guild.id,))
        await ctx.reply("DELETED RULES")
        await db.commit()