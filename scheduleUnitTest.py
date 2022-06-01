from unittest import IsolatedAsyncioTestCase
import unittest
import scheduleFunctions
from datetime import datetime , date, timedelta 
import tables
import aiosqlite

TESTID = 1 #Going under assumption that no discord server has guild id of TESTID
EXPECTEDSCHEDULES = 1
TESTTIME = 5
TIMEFORMAT = "%m/%d/%Y %H:%M"
DBFILE = "main.db"
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

class ScheduleTests(IsolatedAsyncioTestCase):

    async def check_db_entry(self, guild_id, name):
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT guild, timeBetween, alarmTime, currentIndex, message, list FROM schedulesTable WHERE guild = ? AND message = ?", (guild_id, name))
                return await cursor.fetchone()  

    async def check_db_time(self,guild_id, name):
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT alarmTime FROM schedulesTable WHERE guild = ? AND message = ?", (guild_id, name))
                return await cursor.fetchone()  

    def test(self):
        self.assertTrue(True)

    def test_convertToMinutes(self):
        self.assertEqual(-1,scheduleFunctions.convertToMinutes("adasdas", 1))
        self.assertEqual(1,scheduleFunctions.convertToMinutes("m", 1))
        self.assertEqual(120,scheduleFunctions.convertToMinutes("hour", 2))
        self.assertEqual(20160,scheduleFunctions.convertToMinutes("week", 2))

    def test_dateConversion(self):
        self.assertEqual( datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M"),scheduleFunctions.dateConversion(""))
        self.assertEqual(-1,scheduleFunctions.dateConversion(None))
        self.assertEqual(-1,scheduleFunctions.dateConversion("5-16-2022 13:01"))

    async def test_insertScheduler(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual("Scheduled a message every 1 m Message: MESSAGE", await scheduleFunctions.insertScheduler(TESTID,TESTTIME,"5-16-2022 13:01","m",1,"MESSAGE",""))
        self.assertEqual(1,await scheduleFunctions.getScheduleNum(TESTID))
        self.assertEqual((1, 5, '5-16-2022 13:01', 0, 'MESSAGE', ''), await self.check_db_entry(TESTID, 'MESSAGE'))
        await scheduleFunctions.clearScheduleFunction(TESTID)

    async def test_deleteScheduleFunctionNone(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual("NO SUCH SCHEDULE ID",await scheduleFunctions.deleteScheduleFunction(TESTID,1))

    async def test_clearSchedulerFunction(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual(0,await scheduleFunctions.getScheduleNum(TESTID))
        await scheduleFunctions.insertScheduler(TESTID,TESTTIME,"5-16-2022 13:01","m",1,"MESSAGE","")
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual(0,await scheduleFunctions.getScheduleNum(TESTID))       

    async def test_getSchedulerFunction(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual("No Schedules Currently",await scheduleFunctions.getScheduleFunction(TESTID))

    async def test_repeatUntilPresentFunction(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        await scheduleFunctions.insertScheduler(TESTID,1,"2022-05-30 12:20:00","m",1,"MESSAGE","")
        await scheduleFunctions.repeatUntilPresentFunction(TESTID)
        currentTime = scheduleFunctions.dateConversion("")
        expectedTime = await self.check_db_time(TESTID,'MESSAGE')
        expectedTime = datetime.strptime(expectedTime[0],DATEFORMAT)
        self.assertEqual(currentTime,expectedTime)
        await scheduleFunctions.clearScheduleFunction(TESTID)
        
if __name__ == '__main__':
    unittest.main()
