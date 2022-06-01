import aiosqlite

async def removeChannelScheduleFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM restrictTable WHERE guild = ? AND category = ?",(id,"schedule"))
        await db.commit()

async def restrictChannelScheduleFunction(id,s):
    await removeChannelScheduleFunction(id)
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT list from restrictTable WHERE guild = ? AND category = ?",(id,"schedule"))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM restrictTable WHERE guild = ? AND category = ?",(id,"schedule"))
            await cursor.execute("INSERT INTO restrictTable (guild,category,list) VALUES (?,?,?)",(id,"schedule",s))
        await db.commit()
    return f"Restrict scheduling announcements to {s}"

async def getRestrictScheduleNum(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM restrictTable WHERE guild = ? AND category = ?",(id,"schedule"))
            data = await cursor.fetchone()
        await db.commit()
    return data[0]