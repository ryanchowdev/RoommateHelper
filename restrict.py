from builtins import bot
import aiosqlite
import discord
import restrictFunctions
 
 
@bot.command()
async def restrictChannelSchedule(ctx, *args):
    s = ' '.join([str(elem) for elem in args])
    channel = discord.utils.get(ctx.guild.text_channels, name=s)
    if channel == None:
        await ctx.reply(f"{s} is not a channel name")
        return
    await ctx.reply(await restrictFunctions.restrictChannelScheduleFunction(ctx.guild.id,s))

@bot.command()
async def removeChannelSchedule(ctx):
    await restrictFunctions.removeChannelScheduleFunction(ctx.guild.id)
    await ctx.reply("Removed channel")