from cgi import test
from unittest import IsolatedAsyncioTestCase
import unittest
import restrictFunctions
import tables
import aiosqlite

DBFILE = "main.db"
TESTID = 1 #Going under assumption that no discord server has guild id of TESTID
EXPECTEDRULES = 1

class RestrictTests(IsolatedAsyncioTestCase):

    async def check_db_entry(self, guild_id):
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT list FROM restrictTable WHERE guild = ? AND category = ?", (guild_id, "schedule"))
                return await cursor.fetchone()  
    
    async def test_restrictChannelSchedule(self):
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        await restrictFunctions.restrictChannelScheduleFunction(TESTID,"test")
        self.assertEqual("test", (await self.check_db_entry(TESTID))[0])
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        
    async def test_restrictChannelScheduleExist(self):
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        await restrictFunctions.restrictChannelScheduleFunction(TESTID,"test1")
        self.assertEqual("test1", (await self.check_db_entry(TESTID))[0])
        await restrictFunctions.restrictChannelScheduleFunction(TESTID,"test2")
        self.assertEqual("test2", (await self.check_db_entry(TESTID))[0])
        await restrictFunctions.removeChannelScheduleFunction(TESTID)

    async def test_removeChannelSchedule(self):
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        self.assertEqual(0,await restrictFunctions.getRestrictScheduleNum(TESTID))
        await restrictFunctions.restrictChannelScheduleFunction(TESTID,"test")
        self.assertEqual(1,await restrictFunctions.getRestrictScheduleNum(TESTID))
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        self.assertEqual(0,await restrictFunctions.getRestrictScheduleNum(TESTID))

if __name__ == '__main__':
    unittest.main()