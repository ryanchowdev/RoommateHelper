import os
from pathlib import Path
from builtins import bot
import aiosqlite
import discord
 
 
@bot.command()
async def restrictChannelSchedule(ctx, *args):
    s = ' '.join([str(elem) for elem in args])
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT list from restrictTable WHERE guild = ? AND category = ?",(ctx.guild.id,"schedule"))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM restrictTable WHERE guild = ? AND category = ?",(ctx.guild.id,"schedule"))
            channel = discord.utils.get(ctx.guild.text_channels, name=s)
            if channel == None:
                await ctx.reply(f"{s} is not a channel name")
                return
            await cursor.execute("INSERT INTO restrictTable (guild,category,list) VALUES (?,?,?)",(ctx.guild.id,"schedule",s))
        await ctx.reply(f"Restrict scheduling announcements to {s}")
        await db.commit()

@bot.command()
async def removeChannelSchedule(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM restrictTable WHERE guild = ? AND category = ?",(ctx.guild.id,"schedule"))
        await db.commit()