from builtins import bot
import listsFunctions

DBFILE = "main.db"

@bot.command()
async def addlist(ctx, name:str, *note):
    """Adds note to the list with name. Creates the list if it does not exist.
        Usage: addlist name note"""
    try:
        my_note = " ".join(note)
        if not my_note:
            await ctx.reply("Please provide a note to add to the list.")
        else:
            await ctx.reply(await listsFunctions.list_add(name, my_note, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: addlist name note")

@bot.command()
async def editlist(ctx, name:str, id, *note):
    """Edits the note at id in the named list.
        Usage: editlist name id note"""
    try:
        my_note = " ".join(note)
        if not my_note:
            await ctx.reply("Please provide a note to add to the list.")
        else:
            await ctx.reply(await listsFunctions.list_edit(name, id, my_note, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: editlist name id note")

@bot.command()
async def removelist(ctx, name:str, id=-1):
    """Removes the note at id in the named list.
        If no id is provided, remove the named list.
        Usage: removelist name id"""
    try:
        await ctx.reply(await listsFunctions.list_remove(name, id, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: removelist name id")

@bot.command()
async def clearlist(ctx):
    """Delete all lists.
        Usage: clearlist"""
    try:
        await ctx.reply(await listsFunctions.list_clear(ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: clearlist")

@bot.command()
async def checklist(ctx, name:str=""):
    """Check the named list. If no name provided, check all lists.
        Usage: checklist name(optional)"""
    try:
        await ctx.reply(await listsFunctions.list_check(name, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: checklist name(optional)")