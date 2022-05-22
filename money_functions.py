import aiosqlite

DBFILE = "main.db"

async def set_debt(name, amt, note, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get debt for name
            await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (guild_id, name))
            data = await cursor.fetchone()
            if data:
                # Update if record exists
                await cursor.execute("UPDATE moneyTable SET amount = ?, reason = ? WHERE guild = ? AND person = ?", (amt, note, guild_id, name))
            else:
                # Insert if record does not exist
                await cursor.execute("INSERT INTO moneyTable (guild,person,amount,reason) VALUES (?,?,?,?)", (guild_id, name, amt, note))
            await db.commit()
    return f"Added debt for {name} of amount ${amt:.2f} with note: {note}."

async def change_debt(name, amt, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            new_debt = 0
            # Get debt for name
            await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (guild_id, name))
            data = await cursor.fetchone()
            if data:
                current_debt = data[2]
                new_debt = max(current_debt + amt, 0.00)
                # Update if record exists
                await cursor.execute("UPDATE moneyTable SET amount = ? WHERE guild = ? AND person = ?", (new_debt, guild_id, name))
            else:
                new_debt = amt
                # Insert if record does not exist
                await cursor.execute("INSERT INTO moneyTable (guild,person,amount) VALUES (?,?,?)", (guild_id, name, new_debt))
            await db.commit()
    return f"Adjusted debt for {name} by {amt:.2f}. New debt: {new_debt:.2f}."

async def change_note(name, note, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get debt for name
            await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (guild_id, name))
            data = await cursor.fetchone()
            if data:
                # Update if record exists
                await cursor.execute("UPDATE moneyTable SET reason = ? WHERE guild = ? AND person = ?", (note, guild_id, name))
            else:
                # Insert if record does not exist
                await cursor.execute("INSERT INTO moneyTable (guild,person,reason) VALUES (?,?,?)", (guild_id, name, note))
            await db.commit()
    return f"Adjusted note for {name}. New note: {note}."

async def check_debt(guild_id):
    message = ""
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get debts for current server
            await cursor.execute("SELECT * FROM moneyTable WHERE guild = ?", (guild_id,))
            data = await cursor.fetchall()
            if data:
                message = "**Current Debts**\n"
                for d in data:
                    message += f"{d[1]} owes ${str(d[2])}. Note: {d[3]}\n"
            else:
                message = "No current debts."
    return message

async def clear_debt(guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Delete records for this guild
            await cursor.execute("DELETE FROM moneyTable WHERE guild = ?", (guild_id,))
        await db.commit()
    return "All debts cleared."

async def remove_debt(name, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get debt for name
            await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (guild_id, name))
            data = await cursor.fetchone()
            if data:
                # Delete record for this name
                await cursor.execute("DELETE FROM moneyTable WHERE guild = ? AND person = ?", (guild_id, name))
                await db.commit()
                return f"Removed debt for {name}."
            else:
                return f"{name} did not have any debt."

