from builtins import bot
import gmapsFunctions

@bot.command()
async def places(ctx):
    """
    replies to the user with the queried places
    """
    cmd = ctx.message.content.split(" ")
    await ctx.reply(gmapsFunctions.places(cmd[1:]))