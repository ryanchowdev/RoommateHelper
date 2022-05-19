import os
import aiosqlite
import urllib3
import json
from builtins import bot

DBFILE = "main.db"

def getPlaces(query):
    """returns a URL with the queried places."""
    URL = f"https://www.google.com/maps/search/?api=1&query={query}"
    return URL


@bot.command()
async def places(ctx):
    """
    replies to the user with the queried places
    """
    cmd = ctx.message.content.split(" ")
    query = " ".join(cmd[1:])
    if query is None:
        await ctx.reply("Please enter a query by `=places <query>`, ex: =places coffee shop")
    else:
        await ctx.reply(getPlaces(query))
