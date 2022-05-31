import aiosqlite
import urllib3
import json

#sqlite
DBFILE = "main.db"

# https://openweathermap.org/api - Free weather API

units = {"imperial": {"temp": "F", "wind": "mi/h"},
         "metric": {"temp": "C", "wind": "m/s"}}

def getWeather(city, unit_sys, openweather_key):
    """returns a string describing the current weather in the specified city."""
    WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=%s" % (
        city, openweather_key, unit_sys)
    with urllib3.PoolManager() as http:
      r = http.request('GET', WEATHER_API)
      if r.status != 200:
          return "Error retrieving weather data: HTTP error %s" % r.status
      data = json.loads(r.data.decode('utf-8'))
    if unit_sys != "metric" and unit_sys != "imperial":
        return "Error retrieving weather data: invalid unit system"
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

async def setCity(city, guildId):
    """
    sets and locally saves the user specified city for specified guild
    """
    # update sqlite db
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM localeTable WHERE guild = ?", (guildId,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE localeTable SET city = ? WHERE guild = ?", (city, guildId))
            else:
                await cursor.execute("INSERT INTO localeTable (guild,city) VALUES (?, ?)", (guildId, city))
            await db.commit()
    return f"Location set to {city}"


async def setUnits(unit_sys, guildId):
    """
    sets and locally saves the user specified temperature unit for specified guild
    """
    # update sqlite db
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM localeTable WHERE guild = ?", (guildId,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE localeTable SET unit_sys = ? WHERE guild = ?", (unit_sys, guildId))
            else:
                await cursor.execute("INSERT INTO localeTable (guild,unit_sys) VALUES (?, ?)", (guildId, unit_sys))
            await db.commit()
    return f"Units set to {unit_sys}"


async def weather(guildId, openweather_key):
    """
    pulls city and unit_sys from sqlite db and calls getWeather(), returns weather msg
    """
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM localeTable WHERE guild = ?",(guildId,))
            await db.commit()
            data = await cursor.fetchone()
            if data:
                city = data[1]
                # get unit system from db, default to imperial
                unit_sys = data[2] if data[2] else 'imperial'
                return getWeather(city, unit_sys, openweather_key)
            else:
                return "Please set your city first with `=setCity <city>`"