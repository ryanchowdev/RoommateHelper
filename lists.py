from builtins import bot
import listsFunctions

DBFILE = "main.db"

@bot.command()
async def listadd(ctx, name:str, *note):
    """Adds note to the list with name. Creates the list if it does not exist.
        Usage: listadd name note"""
    try:
        my_note = " ".join(note)
        if not my_note:
            await ctx.reply("Please provide a note to add to the list.")
        else:
            await ctx.reply(await listsFunctions.list_add(name, my_note, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: list name note")

@bot.command()
async def listedit(ctx, name:str, id, *note):
    """Edits the note at id in the named list.
        Usage: listedit name id note"""
    try:
        my_note = " ".join(note)
        if not my_note:
            await ctx.reply("Please provide a note to add to the list.")
        else:
            await ctx.reply(await listsFunctions.list_edit(name, id, my_note, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: listedit name id note")

@bot.command()
async def listremove(ctx, name:str, id):
    """Removes the note at id in the named list.
        Usage: listremove name id"""
    try:
        await ctx.reply(await listsFunctions.list_remove(name, id, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: listremove name id")

@bot.command()
async def listdelete(ctx, name:str):
    """Deletes the named list.
        Usage: listdelete name"""
    try:
        await ctx.reply(await listsFunctions.list_delete(name, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: listdelete name")

@bot.command()
async def listclear(ctx):
    """Delete all lists.
        Usage: listclear"""
    try:
        await ctx.reply(await listsFunctions.list_clear(ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: listclear")

@bot.command()
async def listcheck(ctx, name:str=""):
    """Check the named list. If no name provided, check all lists.
        Usage: listcheck name(optional)"""
    try:
        await ctx.reply(await listsFunctions.list_check(name, ctx.guild.id))
    except:
        await ctx.reply("Invalid command. Usage: listcheck name(optional)")