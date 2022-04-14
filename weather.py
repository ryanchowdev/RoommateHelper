import os
import pickle
import urllib3
import json
from builtins import bot

OPENWEATHER_KEY = os.getenv('OPENWEATHER_KEY')

try:
    user_data = pickle.load(open("user_data.p", "rb"))
except:
    user_data = {'user_city': None, 'unit': 'F'}
    pickle.dump(user_data, open("user_data.p", "wb"))

def getWeather(city):
    units = "imperial" if user_data['unit'] == 'F' else "metric"
    WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=%s" % (city, OPENWEATHER_KEY, units)
    http = urllib3.PoolManager()
    r = http.request('GET', WEATHER_API)
    data = json.loads(r.data.decode('utf-8'))
    city = data['name']
    conditions = data['weather'][0]['description']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather_response = "In %s, it's %s °%s out, but feels like %s °%s.\nCurrent conditions: %s \n" % (city, temp, user_data["unit"], feels_like, user_data["unit"], conditions)
    return weather_response

@bot.command()
async def setCity(ctx):
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
    global user_data
    cmd = ctx.message.content.split(" ")
    if len(cmd) != 2:
        await ctx.reply("Usage:\n`=setUnits (F)ahrenheit OR (C)elsius`")
    else:
        if cmd[1][0].upper() == 'F':
            user_data['unit'] = 'F'
        elif cmd[1][0].upper() == 'C':
            user_data['unit'] = 'C'
        else:
            await ctx.reply("Usage:\n`=setUnits (F)ahrenheit OR (C)elsius`")
            return
        user_data['units'] = " ".join(cmd[1:])
        pickle.dump(user_data, open("user_data.p", "wb"))
        await ctx.reply("Units set to " + user_data['units'])


@bot.command()
async def weather(ctx):
    if user_data['user_city'] is None:
        await ctx.reply("Please set your city first with `=setCity <city>`")
    else:
        await ctx.reply(getWeather(user_data['user_city']))
    