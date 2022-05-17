import os
from pathlib import Path
from builtins import bot
import aiosqlite
import rulesFunctions  


@bot.command()
async def addRule(ctx, *args):
    rule = ""
    for i in args:
        rule += f"{i} "
    s = await rulesFunctions.addRuleCommand(ctx.guild.id,rule)
    await ctx.reply(s)


@bot.command()
async def getRules(ctx):
    await ctx.reply(await rulesFunctions.getRulesCommand(ctx.guild.id))

@bot.command()
async def clearRules(ctx):
    await rulesFunctions.clearRulesCommand(ctx.guild.id)
    await ctx.reply("DELETED RULES")
        
@bot.command()
async def numRules(ctx):
    await ctx.reply(f"Number of rules is {await rulesFunctions.getNumRulesCommand(ctx.guild.id)}")