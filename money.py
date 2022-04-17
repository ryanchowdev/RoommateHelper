import os
import pickle
from pathlib import Path
from builtins import bot

def save_to_file(dict, f):
    debts_file = open(f, 'bw+')
    pickle.dump(dict, debts_file)
    debts_file.close()

def load_from_file(f):
    # create pickle file if it does not exist
    myfile = Path(f)
    myfile.touch(exist_ok=True)
    # load
    debts_file = open(myfile, 'br')
    debts = pickle.load(debts_file)
    debts_file.close()
    return debts

def record_debt(name, amt):
    # create pickle file if it does not exist
    myfile = Path('debts.pkl')
    myfile.touch(exist_ok=True)
    # only load from pickle file if it is nonempty
    debts = load_from_file('debts.pkl') if os.stat('debts.pkl').st_size != 0 else {}
    debts.update({name: amt})
    save_to_file(debts, 'debts.pkl')

@bot.command()
async def debt(ctx, name:str, amt:float=0):
    rounded_amt = round(amt, 2)
    record_debt(name, rounded_amt)
    await ctx.reply(f"Added debt for {name} of amount ${rounded_amt:.2f}.")

# Will probably make this part of debt command later
@bot.command()
async def checkdebt(ctx):
    try:
        if os.stat('debts.pkl').st_size != 0:
            message = ""
            debts = load_from_file('debts.pkl')
            for key in debts:
                message += f"{key} owes ${str(debts[key])}.\n"
            await ctx.reply(f"Current debts:\n{message}")
        else:
            await ctx.reply(f"No current debts.")
    except:
        await ctx.reply(f"No current debts.")

# Will probably make this part of debt command later
@bot.command()
async def cleardebt(ctx):
    open("debts.pkl", "w").close()
    await ctx.reply(f"All debts cleared.")

# Features to be added
# Increment/decrement existing debt instead of overwriting with new value
# Clear debt for individual person