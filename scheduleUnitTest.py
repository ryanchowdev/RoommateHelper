from unittest import IsolatedAsyncioTestCase
import unittest
import scheduleFunctions
from datetime import datetime , date, timedelta 

TESTID = 1 #Going under assumption that no discord server has guild id of TESTID
EXPECTEDSCHEDULES = 1
TESTTIME = 5
TIMEFORMAT = "%m/%d/%Y %H:%M"

class ScheduleTests(IsolatedAsyncioTestCase):

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
        self.assertEqual(-1,scheduleFunctions.dateConversion("5/16/2022 13:01"))

    async def test_insertScheduler(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual("Scheduled a message every 1 m Message: MESSAGE", await scheduleFunctions.insertScheduler(TESTID,TESTTIME,"5/16/2022 13:01","m",1,"MESSAGE",""))
        self.assertEqual(1,await scheduleFunctions.getScheduleNum(TESTID))
        await scheduleFunctions.clearScheduleFunction(TESTID)

    async def test_clearSchedulerFunction(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual(0,await scheduleFunctions.getScheduleNum(TESTID))
        await scheduleFunctions.insertScheduler(TESTID,TESTTIME,"5/16/2022 13:01","m",1,"MESSAGE","")
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual(0,await scheduleFunctions.getScheduleNum(TESTID))       

    async def test_getSchedulerFunction(self):
        await scheduleFunctions.clearScheduleFunction(TESTID)
        self.assertEqual("No Schedules Currently",await scheduleFunctions.getScheduleFunction(TESTID))
        
if __name__ == '__main__':
    unittest.main()