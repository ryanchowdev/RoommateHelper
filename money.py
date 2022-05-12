import os
import pickle
import aiosqlite
from pathlib import Path
from builtins import bot

DBFILE = "main.db"

@bot.command()
async def debt(ctx, name:str, amt):
    try:
        amt = round(float(amt), 2)
        assert amt > 0
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                # get debt for name
                await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (ctx.guild.id, name))
                data = await cursor.fetchone()
                if data:
                    # update if record exists
                    await cursor.execute("UPDATE moneyTable SET amount = ? WHERE guild = ? AND person = ?", (amt, ctx.guild.id, name))
                else:
                    # insert if record does not exist
                    await cursor.execute("INSERT INTO moneyTable (guild,person,amount) VALUES (?,?,?)", (ctx.guild.id, name, amt))
                await db.commit()
                await ctx.reply(f"Added debt for {name} of amount ${amt:.2f}.")
    except AssertionError:
        await ctx.reply("Debt amount must be positive (>0).")
    except:
        await ctx.reply("Invalid command. Usage: debt name amount")

@bot.command()
async def changedebt(ctx, name:str, amt):
    try:
        amt = round(float(amt), 2)
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                new_debt = 0
                # get debt for name
                await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (ctx.guild.id, name))
                data = await cursor.fetchone()
                if data:
                    current_debt = data[2]
                    new_debt = max(current_debt + amt, 0.00)
                    # update if record exists
                    await cursor.execute("UPDATE moneyTable SET amount = ? WHERE guild = ? AND person = ?", (new_debt, ctx.guild.id, name))
                else:
                    new_debt = amt
                    # insert if record does not exist
                    await cursor.execute("INSERT INTO moneyTable (guild,person,amount) VALUES (?,?,?)", (ctx.guild.id, name, new_debt))
                await db.commit()
                await ctx.reply(f"Adjusted debt for {name} by {amt:.2f}. New debt: {new_debt:.2f}")
    except:
        await ctx.reply("Invalid command. Usage: changedebt name amount")

@bot.command()
async def checkdebt(ctx):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # get debts for current server
            await cursor.execute("SELECT * FROM moneyTable WHERE guild = ?", (ctx.guild.id,))
            data = await cursor.fetchall()
            if data:
                message = "**Current Debts**\n"
                for d in data:
                    message += f"{d[1]} owes ${str(d[2])}.\n"
                await ctx.reply(message)
            else:
                await ctx.reply("No current debts.")

@bot.command()
async def cleardebt(ctx):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # delete records for this guild
            await cursor.execute("DELETE FROM moneyTable WHERE guild = ?", (ctx.guild.id,))
        await db.commit()
        await ctx.reply("All debts cleared.")
