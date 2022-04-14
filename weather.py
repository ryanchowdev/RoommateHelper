import os
import pickle
import urllib3
import json
from builtins import bot

# https://openweathermap.org/api - Free weather API
OPENWEATHER_KEY = os.getenv('OPENWEATHER_KEY')

# using pickle to save/reload data
# https://docs.python.org/3/library/pickle.html
try:
    user_data = pickle.load(open("user_data.p", "rb"))
except:
    user_data = {'user_city': None, 'unit_sys': 'imperial'}
    pickle.dump(user_data, open("user_data.p", "wb"))

units = {"imperial": {"temp": "F", "wind": "mi/h"},
         "metric": {"temp": "C", "wind": "m/s"}}


def getWeather(city):
    """returns a string describing the current weather in the specified city."""
    unit_sys = user_data['unit_sys']
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
    global user_data
    cmd = ctx.message.content.split(" ")
    if len(cmd) == 1:
        await ctx.reply("Usage:\n`=setCity <city>`")
    else:
        user_data['user_city'] = " ".join(cmd[1:])
        pickle.dump(user_data, open("user_data.p", "wb"))
        await ctx.reply("Location set to " + user_data['user_city'])


@bot.command()
async def setUnits(ctx):
    """
    sets and locally saves the user specified temperature unit
    """
    global user_data
    cmd = ctx.message.content.split(" ")
    if len(cmd) != 2:
        await ctx.reply("Usage:\n`=setUnits (F)ahrenheit OR (C)elsius`")
        return
    unit = cmd[1][0].upper()
    if unit == 'F' or unit == 'C':
        user_data['unit'] = unit
        pickle.dump(user_data, open("user_data.p", "wb"))
        await ctx.reply("Units set to " + unit)
    else:
        await ctx.reply("Usage:\n`=setUnits (F)ahrenheit OR (C)elsius`")
        return


@bot.command()
async def weather(ctx):
    """
    replies to the user with the current weather in their city
    """
    if user_data['user_city'] is None:
        await ctx.reply("Please set your city first with `=setCity <city>`")
    else:
        await ctx.reply(getWeather(user_data['user_city']))
