import os
from re import A
import discord
from discord.ext import commands

def displayHeads():
    embed=discord.Embed(
        title="RoommateHelper : Coin Flip", 
        description="",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="You got:", 
        value="Heads", 
        inline=False
    )
    embed.set_image(url="https://i.imgur.com/DsLFwRO.png")
    
    return embed

def displayTails():
    embed=discord.Embed(
        title="RoommateHelper : Coin Flip", 
        description="",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="You got:", 
        value="Tails", 
        inline=False
    )
    embed.set_image(url="https://i.imgur.com/3Xqr7Eh.png")
    
    return embed
    