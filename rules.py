import os
from pathlib import Path
from builtins import bot
import aiosqlite
import rulesFunctions  


@bot.command()
async def addRule(ctx, *args):
    """Adds a rule to the ruleboard for the server. Usage: addRule Dont litter"""
    rule = ""
    for i in args:
        rule += f"{i} "
    s = await rulesFunctions.addRuleCommand(ctx.guild.id,rule)
    await ctx.reply(s)


@bot.command()
async def getRules(ctx):
    """prints the current server rules. Usage: getRules"""
    await ctx.reply(await rulesFunctions.getRulesCommand(ctx.guild.id))

@bot.command()
async def clearRules(ctx):
    """Clears the rule board for the server. Usage: clearRules"""
    await rulesFunctions.clearRulesCommand(ctx.guild.id)
    await ctx.reply("DELETED RULES")
        
@bot.command()
async def numRules(ctx):
    """Returns the amount of rules there currently are. Usage: numRules"""
    await ctx.reply(f"Number of rules is {await rulesFunctions.getNumRulesCommand(ctx.guild.id)}")