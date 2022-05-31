import aiosqlite

DBFILE = "main.db"

async def list_add(name, note, guild_id):
    my_id = 0
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get list for name
            await cursor.execute("SELECT * FROM listsTable WHERE guild = ? AND name = ?", (guild_id, name))
            data = await cursor.fetchone()
            if data:
                # The list exists
                # First calculate the note id = current highest id + 1
                await cursor.execute("SELECT MAX(postid) FROM listsTable WHERE guild = ? AND name = ?", (guild_id, name))
                result = await cursor.fetchone()
                my_id = result[0] + 1
                # Now add note to the list
                await cursor.execute("INSERT INTO listsTable (guild,name,postid,note) VALUES (?,?,?,?)", (guild_id, name, my_id, note))
            else:
                # The list does not exist, so create it and add note
                my_id = 1
                await cursor.execute("INSERT INTO listsTable (guild,name,postid,note) VALUES (?,?,?,?)", (guild_id, name, my_id, note))
            await db.commit()
    return f"Added to list \"{name}\" the note:\n{my_id}) {note}"

async def list_edit(name, post_id, note, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get post in named list
            await cursor.execute("SELECT * FROM listsTable WHERE guild = ? AND name = ? AND postid = ?", (guild_id, name, post_id))
            data = await cursor.fetchone()
            if data:
                # The post exists
                await cursor.execute("UPDATE listsTable SET note = ? WHERE guild = ? AND name = ? AND postid = ?", (note, guild_id, name, post_id))
            else:
                # Post or list does not exist, so tell user to use listadd instead
                return f"Unable to find a note with id {post_id} in list {name}. Create the note using listadd name note."
            await db.commit()
    return f"Edited note {post_id} in list {name} to: {note}"

async def list_remove(name, post_id, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get the post from the list
            await cursor.execute("SELECT * FROM listsTable WHERE guild = ? AND name = ? AND postid = ?", (guild_id, name, post_id))
            data = await cursor.fetchone()
            if data:
                # Delete post for this list
                await cursor.execute("DELETE FROM listsTable WHERE guild = ? AND name = ? AND postid = ?", (guild_id, name, post_id))
                await db.commit()
                return f"Removed post {post_id} from list: {name}."
            else:
                return f"Did not find post {post_id} in list: {name}."

async def list_delete(name, guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Get named list
            await cursor.execute("SELECT * FROM listsTable WHERE guild = ? AND name = ?", (guild_id, name))
            data = await cursor.fetchall()
            if data:
                # Delete list
                await cursor.execute("DELETE FROM listsTable WHERE guild = ? AND name = ?", (guild_id, name))
                await db.commit()
            else:
                return f"Did not find list: {name}."
    return f"Deleted list: {name}."

async def list_clear(guild_id):
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # Deletes all lists for this guild
            await cursor.execute("DELETE FROM listsTable WHERE guild = ?", (guild_id,))
        await db.commit()
    return "All lists cleared."

async def list_check(name, guild_id):
    msg = ""
    async with aiosqlite.connect(DBFILE) as db:
        async with db.cursor() as cursor:
            # If name was provided, get the named list
            if name:
                await cursor.execute("SELECT * FROM listsTable WHERE guild = ? AND name = ?", (guild_id, name))
                data = await cursor.fetchall()
                if data:
                    msg = f"**Showing List: {name}**\n"
                    for d in data:
                        msg += f"{d[2]}) {d[3]}\n"  # d[2]: postid, d[3]: note
                else:
                    msg = f"Could not find notes in list: {name}"
            # Else get all records for this guild
            else:
                await cursor.execute("SELECT * FROM listsTable WHERE guild = ?", (guild_id,))
                data = await cursor.fetchall()
                if data:
                    msg = f"**Showing All Lists**\n"
                    cur_list = ""
                    for d in data:
                        if d[1] != cur_list:
                            msg += f"__List: {d[1]}__\n"  # d[1]: list name
                            cur_list = d[1]
                        msg += f"{d[2]}) {d[3]}\n"  # d[2]: postid, d[3]: note
                else:
                    msg = "No lists found."
    return msg
