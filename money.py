from builtins import bot
import money_functions

DBFILE = "main.db"

@bot.command()
async def debt(ctx, name:str, amt, *note):
    """Set debt for a person. Usage: debt name amt note(optional)"""
    try:
        amt = round(float(amt), 2)
        assert amt > 0
        my_note = " ".join(note) if len(note) > 0 else "No note provided"
        await ctx.reply(await money_functions.set_debt(name, amt, my_note, ctx.guild.id))
    except AssertionError:
        await ctx.reply("Debt amount must be positive (>0).")
    except:
        await ctx.reply("Invalid command. Usage: debt name amount note(optional)")

@bot.command()
async def changedebt(ctx, name:str, amt):
    """Change debt for a person. Usage: name amt"""
    try:
        amt = round(float(amt), 2)
        await ctx.reply(await money_functions.change_debt(name, amt, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: changedebt name amount")

@bot.command()
async def changenote(ctx, name:str, *note):
    """Change note for a person. Usage: changenote name note"""
    my_note = " ".join(note)
    try:
        await ctx.reply(await money_functions.change_note(name, my_note, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: changenote name note")

@bot.command()
async def checkdebt(ctx):
    """Check all debts. Usage: checkdebt"""
    try:
        await ctx.reply(await money_functions.check_debt(ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: checkdebt")

@bot.command()
async def cleardebt(ctx):
    """Clear all debts. Usage: cleardebt"""
    try:
        await ctx.reply(await money_functions.clear_debt(ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: cleardebt")

@bot.command()
async def removedebt(ctx, name:str):
    """Remove debt for a person. Usage: removedebt name"""
    try:
        await ctx.reply(await money_functions.remove_debt(name, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: removedebt name")
