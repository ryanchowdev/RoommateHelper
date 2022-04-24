import os
from pathlib import Path
from builtins import bot
import aiosqlite
        
@bot.command()
async def addRule(ctx, *args):
    rule = ""
    for i in args:
        rule += f"{i} "
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT rules from rulesTable WHERE guild = ? AND rules = ?",(ctx.guild.id,rule))
            data = await cursor.fetchone()
            if data:
                await ctx.reply(f"Rule already exists: {rule}")
            else:
                await cursor.execute("INSERT INTO rulesTable (rules,guild) VALUES (?,?)",(rule,ctx.guild.id))
                await ctx.reply(f"Rule added: {rule}")
        await db.commit()

@bot.command()
async def getRules(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT rules from rulesTable WHERE guild = ?",(ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                string = "RULES\n"
                num = 1
                for i in data:
                    string += f"{num}. {(i[0])} \n"
                    num+=1
                await ctx.reply(string)
            else:
                await ctx.reply(" NO RULES CURRENTLY")

@bot.command()
async def clearRules(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM rulesTable WHERE guild = ?",(ctx.guild.id,))
        await ctx.reply("DELETED RULES")
        await db.commit()