import os
import aiosqlite
import urllib3
import json
from builtins import bot

#sqlite
DBFILE = "main.db"

# https://openweathermap.org/api - Free weather API
OPENWEATHER_KEY = os.getenv('OPENWEATHER_KEY')

units = {"imperial": {"temp": "F", "wind": "mi/h"},
         "metric": {"temp": "C", "wind": "m/s"}}


def getWeather(city, unit_sys):
    """returns a string describing the current weather in the specified city."""
    WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=%s" % (
        city, OPENWEATHER_KEY, unit_sys)
    http = urllib3.PoolManager()
    r = http.request('GET', WEATHER_API)
    if r.status != 200:
        return "Error retrieving weather data: HTTP error %s" % r.status
    data = json.loads(r.data.decode('utf-8'))
    temp_unit = units[unit_sys]['temp']
    wind_unit = units[unit_sys]['wind']
    city = data['name']
    conditions = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_max = data['main']['temp_max']
    temp_min = data['main']['temp_min']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    weather_response = "In ***%s***, it's **%s °%s** out, but it **feels like %s °%s**.\n*Temperatures will range from %s °%s - %s °%s.*\n*Humidity is at %s%% and wind is blowing at %s %s*.\nCurrent conditions: **%s**" % (
        city, temp, temp_unit, feels_like, temp_unit, temp_min, temp_unit, temp_max, temp_unit, humidity, wind, wind_unit, conditions)
    return weather_response


@bot.command()
async def setCity(ctx):
    """
    sets and locally saves the user specified city
    """
    cmd = ctx.message.content.split(" ")
    if len(cmd) == 1:
        await ctx.reply("Usage:\n`=setCity <city>`")
    else:
        city = " ".join(cmd[1:])
        # update sqlite db
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM localeTable WHERE guild = ?", (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute("UPDATE localeTable SET city = ? WHERE guild = ?", (city, ctx.guild.id))
                else:
                    await cursor.execute("INSERT INTO localeTable (guild,city) VALUES (?, ?)", (ctx.guild.id, city))
                await db.commit()
        await ctx.reply(f"Location set to {city}")


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

    # update sqlite db
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM localeTable WHERE guild = ?", (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE localeTable SET unit_sys = ? WHERE guild = ?", (unit_sys, ctx.guild.id))
            else:
                await cursor.execute("INSERT INTO localeTable (guild,unit_sys) VALUES (?, ?)", (ctx.guild.id, unit_sys))
            await db.commit()
    await ctx.reply(f"Units set to {unit_sys}")


@bot.command()
async def weather(ctx):
    """
    replies to the user with the current weather in their city
    """
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM localeTable WHERE guild = ?",(ctx.guild.id,))
            await db.commit()
            data = await cursor.fetchone()
            if data:
                city = data[1]
                # get unit system from db, default to imperial
                unit_sys = data[2] if data[2] else 'imperial'
                await ctx.reply(getWeather(city, unit_sys))
            else:
                await ctx.reply("Please set your city first with `=setCity <city>`")