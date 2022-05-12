import os
import pickle
import aiosqlite
from pathlib import Path
from builtins import bot

DBFILE = "main.db"

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

def my_debt(name):
    try:
        if os.stat('debts.pkl').st_size != 0:
            debts = load_from_file('debts.pkl')
            return debts[name]
        else:
            return -1
    except:
        return -1

@bot.command()
async def debt(ctx, name:str, amt):
    try:
        amt = float(amt)
        assert amt > 0
        rounded_amt = round(amt, 2)
        record_debt(name, rounded_amt)
        await ctx.reply(f"Added debt for {name} of amount ${rounded_amt:.2f}.")
        # async with aiosqlite.connect(DBFILE) as db:
        #     async with db.cursor() as cursor:
    except AssertionError:
        await ctx.reply("Debt amount must be positive (>0).")
    except:
        await ctx.reply("Invalid command. Usage: debt name amount")

@bot.command()
async def changedebt(ctx, name:str, amt):
    try:
        amt = float(amt)
        rounded_amt = round(amt, 2)
        current_debt = my_debt(name)
        new_debt = 0
        if current_debt == -1:
            new_debt = max(rounded_amt, 0.00)
        else:
            new_debt = max(current_debt + rounded_amt, 0.00) # no negative debt
        record_debt(name, new_debt)
        await ctx.reply(f"Adjusted debt for {name} by {rounded_amt:.2f}. New debt: {new_debt:.2f}")
    except:
        await ctx.reply("Invalid command. Usage: changedebt name amount")

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
            await ctx.reply("No current debts.")
    except:
        await ctx.reply("No current debts.")

@bot.command()
async def cleardebt(ctx):
    open("debts.pkl", "w").close()
    await ctx.reply("All debts cleared.")
