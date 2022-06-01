from builtins import bot
import weatherFunctions
import os
OPENWEATHER_KEY = os.getenv('OPENWEATHER_KEY')

@bot.command()
async def setCity(ctx):
    """
    sets and locally saves the user specified city
    """
    cmd = ctx.message.content.split(" ")
    if len(cmd) == 1:
        return "Usage:\n`=setCity <city>`"
    else:
        city = " ".join(cmd[1:])
    msg = await weatherFunctions.setCity(city, ctx.guild.id)
    await ctx.reply(msg)

@bot.command()
async def setUnits(ctx):
    """
    sets and locally saves the user specified temperature unit
    """
    cmd = ctx.message.content.split(" ")
    if len(cmd) != 2:
        await ctx.reply("Usage:\n`=setUnits (i)mperial OR (m)etric`")
        return
    unit = cmd[1][0].lower()
    if unit == 'i':
        unit_sys = 'imperial'
    elif unit == 'm':
        unit_sys = 'metric'
    else:
        await ctx.reply("Usage:\n`=setUnits (i)mperial OR (m)etric`")
        return
    msg = await weatherFunctions.setUnits(unit_sys, ctx.guild.id)
    await ctx.reply(msg)


@bot.command()
async def weather(ctx):
    """
    replies to the user with the current weather in their city
    """
    msg = await weatherFunctions.weather(ctx.guild.id, OPENWEATHER_KEY)
    await ctx.reply(msg)