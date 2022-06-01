import unittest
import aiosqlite
import alarmFunctions
import tables
from unittest import IsolatedAsyncioTestCase
TESTID = 1


class AlarmTests(IsolatedAsyncioTestCase):

	async def check_db_entry(self, guild_id, event):
		await tables.create_tables()
		async with aiosqlite.connect("main.db") as db:
			async with db.cursor() as cursor:
				await cursor.execute("SELECT * FROM alarmsTable WHERE guild = ? AND event = ?", (guild_id, event))
				return await cursor.fetchone()

	def test(self):
		self.assertTrue(True)

	async def test_alarm(self):
		await alarmFunctions.clearalarm(TESTID)
		await alarmFunctions.alarm('Event1', '7/22/2019' ,'15:00', TESTID)
		result = await self.check_db_entry(TESTID, 'Event1')
		self.assertEqual('Event1', result[1])
		self.assertEqual('7/22/2019', result[2])
		self.assertEqual('15:00', result[3])
		await alarmFunctions.alarm('Event2', '7/25/2019' ,'17:00', TESTID)
		result = await self.check_db_entry(TESTID, 'Event2')
		self.assertEqual('Event2', result[1])
		self.assertEqual('7/25/2019', result[2])
		self.assertEqual('17:00', result[3])
		
	async def test_checkalarm(self):
		await alarmFunctions.clearalarm(TESTID)
		await alarmFunctions.alarm('Event1', '7/22/2019' ,'15:00', TESTID)
		result = await alarmFunctions.checkalarm(TESTID)
		self.assertEqual('Current Alarms\nEvent1 7/22/2019 15:00 \n', result)
		await alarmFunctions.alarm('Event2', '7/25/2019' ,'17:00', TESTID)
		result = await alarmFunctions.checkalarm(TESTID)
		self.assertEqual('Current Alarms\nEvent1 7/22/2019 15:00 \nEvent2 7/25/2019 17:00 \n', result)

	async def test_clearalarm(self):  
		await alarmFunctions.clearalarm(TESTID)
		await alarmFunctions.alarm('Event1', '7/22/2019' ,'15:00', TESTID)
		await alarmFunctions.clearalarm(TESTID)
		result = await alarmFunctions.checkalarm(TESTID)
		self.assertEqual('NO ALARMS CURRENTLY', result)

	async def test_removealarm(self):  	
		await alarmFunctions.clearalarm(TESTID)
		await alarmFunctions.alarm('Event1', '7/22/2019' ,'15:00', TESTID)
		await alarmFunctions.removealarm('Event1',TESTID)
		result = await alarmFunctions.checkalarm(TESTID)
		self.assertEqual('NO ALARMS CURRENTLY', result)

if __name__ == '__main__':
	unittest.main()