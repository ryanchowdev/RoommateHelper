import os
from re import A
import discord
from discord.ext import commands

def displayIntroPage():
    embed=discord.Embed(
        title="RoommateHelper : Help Menu ( = )", 
        description="",
        color=discord.Color.blue()
        )
    
    embed.add_field(
        name="**Alarm**", 
        value="=help alarm", 
        inline=False
        )
    
    embed.add_field(
        name="**Calculator**", 
        value="=help calculator", 
        inline=False
        )
    
    embed.add_field(
        name="**Coin Flip**", 
        value="=help coinflip", 
        inline=False
        )
    
    embed.add_field(
        name="**Google Maps**", 
        value="=help gmaps", 
        inline=False
        )
    
    embed.add_field(
        name="**Money**", 
        value="=help money", 
        inline=False
        )
    
    embed.add_field(
        name="**Polls**", 
        value="=help polls", 
        inline=False
        )
    
    embed.add_field(
        name="**Restrict**", 
        value="=help restrict", 
        inline=False
        )
    
    embed.add_field(
        name="**Rules**", 
        value="=help rules", 
        inline=False
        )
    
    embed.add_field(
        name="**Schedule**", 
        value="=help schedule", 
        inline=False
        )
    
    embed.add_field(
        name="**Weather**", 
        value="=help weather", 
        inline=False
        )
    
    return embed

def displayAlarmPage():
    embed=discord.Embed(
        title="RoommateHelper : Alarm ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**alarm <event> <date> <time>**", 
        value="Schedules a new alarm. Ex: =alarm event 7/22/2019 15:00", 
        inline=False
        )
    
    embed.add_field(
        name="**checkalarm**", 
        value="Checks what alarms are currently scheduled", 
        inline=False
        )
    
    embed.add_field(
        name="**clearalarm**", 
        value="Deletes all scheduled alarms", 
        inline=False
        )
    
    embed.add_field(
        name="**removealarm <event>**", 
        value="Removes the alarm that is specified", 
        inline=False
        )

    return embed

def displayCalculatorPage():
    embed=discord.Embed(
        title="RoommateHelper : Calculator ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**calc <equation>**", 
        value="Calculates an equation and returns an answer. Ex: =calc (9+10)*(56-4)", 
        inline=False
        )
    
    return embed

def displayCoinFlipPage():
    embed=discord.Embed(
        title="RoommateHelper : Coin Flip ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**flip**", 
        value="Returns heads or tails when coin is flipped", 
        inline=False
        )
    
    return embed

def displayGMapsPage():
    embed=discord.Embed(
        title="RoommateHelper : Google Maps ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**places**", 
        value="Replies to the user with queried places", 
        inline=False
        )
    
    return embed

def displayMoneyPage():
    embed=discord.Embed(
        title="RoommateHelper : Money ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**debt <name> <amount> <note>**", 
        value="Set debt for a person. Note is optional", 
        inline=False
        )
    
    embed.add_field(
        name="**changedebt <name> <amount>**", 
        value="Change debt for a person", 
        inline=False
        )
    
    embed.add_field(
        name="**changenote <name> <note>**", 
        value="Change note for a person", 
        inline=False
        )
    
    embed.add_field(
        name="**checkdebt**", 
        value="Checks all debts", 
        inline=False
        )
    
    embed.add_field(
        name="**cleardebt**", 
        value="Clear all debts", 
        inline=False
        )
    
    embed.add_field(
        name="**removedebt <name>**", 
        value="Remove debt for a person", 
        inline=False
        )
    
    return embed

def displayMusicPage():
    embed=discord.Embed(
        title="RoommateHelper : Music ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**musicJoin**", 
        value="Brings the music bot into the Discord voice channel the user is in", 
        inline=False
        )
    
    embed.add_field(
        name="**musicLeave**", 
        value="Makes the music bot leave the Discord voice channel it is in", 
        inline=False
        )
    
    embed.add_field(
        name="**playMusic <url>**", 
        value="Plays music from the URL", 
        inline=False
        )
    
    embed.add_field(
        name="**musicPause**", 
        value="Pauses the music that is currently playing", 
        inline=False
        )
    
    embed.add_field(
        name="**musicResume**", 
        value="Resumes music that is paused", 
        inline=False
        )
    return embed

def displayPollPage():
    embed=discord.Embed(
        title="RoommateHelper : Polls ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**poll**", 
        value="Displays a detailed guide on how to make polls with examples", 
        inline=False
        )
    
    embed.add_field(
        name="**poll <number of options> <message/question> <list of options>**", 
        value="Creates a poll from the given input. Ex: =poll 5 “What pizza do you like?” Cheese Pepperoni “Peanut Butter” Pineapple Combo", 
        inline=False
        )
    
    return embed

def displayRestrictPage():
    embed=discord.Embed(
        title="RoommateHelper : Restrict ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**restrictChannelSchedule <channel>**", 
        value="Restricts scheduling announcements to the one specific channel", 
        inline=False
        )
    
    embed.add_field(
        name="**removeChannelSchedule**", 
        value="Removes channel restriction for scheduling", 
        inline=False
        )
    
    return embed

def displayRulesPage():
    embed=discord.Embed(
        title="RoommateHelper : Rules ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**addRule <new rule>**", 
        value="Adds rule to board", 
        inline=False
        )
    
    embed.add_field(
        name="**getRules**", 
        value="Returns the rules from the ruleboard", 
        inline=False
        )
    
    embed.add_field(
        name="**clearRules**", 
        value="Clears rules from the ruleboard", 
        inline=False
        )
    
    embed.add_field(
        name="**numRules**", 
        value="Gets the amount of rules from the ruleboard", 
        inline=False
        )
    
    return embed

def displaySchedulePage():
    embed=discord.Embed(
        title="RoommateHelper : Schedule ( = )", 
        description="",
        color=discord.Color.blue()
        )

    embed.add_field(
        name="**=schedule <time unit> <amount> “<message>” “list list list” “date”**", 
        value="Creates a schedule based off the given input. Ex: =schedule m 1 “Take out trash” “@user1 @user2 @user3” “5/4/2022 9:40”", 
        inline=False
        )
    
    embed.add_field(
        name="**continueSchedule**", 
        value="Continues schedules. If date for schedule is passed, it repeats itself until the next date", 
        inline=False
        )
    
    embed.add_field(
        name="**stopSchedule**", 
        value="Stops schedule announcements", 
        inline=False
        )
    
    embed.add_field(
        name="**deleteSchedule <id>**", 
        value="Deletes a schedule based on the id. Ex: =deleteSchedule 123456789", 
        inline=False
        )
    
    embed.add_field(
        name="**clearSchedule**", 
        value="Deletes all schedules", 
        inline=False
        )
    
    embed.add_field(
        name="**getSchedule**", 
        value="Gets current schedules and their ids", 
        inline=False
        )
    return embed

def displayWeatherPage():
    embed=discord.Embed(
        title="RoommateHelper : Weather ( = )", 
        description="",
        color=discord.Color.blue()
        )
    
    #embed.set_author(name="RoommateHelper : Weather")
    embed.add_field(
        name="**setCity**", 
        value="Sets and locally saves the user specified city", 
        inline=False
        )
    
    embed.add_field(
        name="**setUnits**", 
        value="Sets and locally saves the user specified temperature unit", 
        inline=False
        )
    
    embed.add_field(
        name="**weather**", 
        value="Replies to the user with the current weather in their city", 
        inline=False
        )
    
    return embed