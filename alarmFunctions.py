import aiosqlite

async def alarm(event, date, time, guild_id):
	async with aiosqlite.connect("main.db") as db:
		async with db.cursor() as cursor:
			await cursor.execute("SELECT * from alarmsTable WHERE guild = ? AND event = ? AND date = ? AND time = ?",(guild_id,event,date, time))
			data = await cursor.fetchone()
			if data:
				return "ALREADY SCHEDULED"
			else:
				await cursor.execute("INSERT INTO alarmsTable (guild,event,date,time) VALUES (?,?,?,?)",(guild_id,event,date,time))
			await db.commit()    
			return f"Added alarm for {event} on {date} at {time}"

async def checkalarm(guild_id):
	async with aiosqlite.connect("main.db") as db:
		async with db.cursor() as cursor:
			await cursor.execute("SELECT * from alarmsTable WHERE guild = ?",(guild_id,))
			data = await cursor.fetchall()
			if data:
				string = "Current Alarms\n"
				for i in data:
					string += f"{(i[1])} {(i[2])} {i[3]} \n"
				return string
			else:
				return "NO ALARMS CURRENTLY"

async def clearalarm(guild_id):
	async with aiosqlite.connect("main.db") as db:
		async with db.cursor() as cursor:
			await cursor.execute("DELETE FROM alarmsTable WHERE guild = ?",(guild_id,))
		await db.commit()
		return "DELETED ALARMS"


async def removealarm(event, guild_id):
	found = False
	async with aiosqlite.connect("main.db") as db:
		async with db.cursor() as cursor:
			await cursor.execute("SELECT * from alarmsTable WHERE guild = ?",(guild_id,))
			data = await cursor.fetchall()
			if data:
				for i in data:
					if(i[1] == event):
					  found = True
					  await cursor.execute("DELETE FROM alarmsTable WHERE guild = ? AND event  = ?" ,(guild_id, i[1]))
					  await db.commit()
					  return "ALARM REMOVED"
					  
	if(found == False):
		return "ALARM NOT FOUND" 

	