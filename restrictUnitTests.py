from cgi import test
from unittest import IsolatedAsyncioTestCase
import unittest
import restrictFunctions

TESTID = 1 #Going under assumption that no discord server has guild id of TESTID
EXPECTEDRULES = 1

class RestrictTests(IsolatedAsyncioTestCase):

    def test(self):
        self.assertTrue(True)
    
    async def test_restrictChannelSchedule(self):
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        self.assertEqual("Restrict scheduling announcements to test",await restrictFunctions.restrictChannelScheduleFunction(TESTID,"test"))
        

    async def test_removeChannelSchedule(self):
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        self.assertEqual(0,await restrictFunctions.getRestrictScheduleNum(TESTID))
        await restrictFunctions.restrictChannelScheduleFunction(TESTID,"test")
        self.assertEqual(1,await restrictFunctions.getRestrictScheduleNum(TESTID))
        await restrictFunctions.removeChannelScheduleFunction(TESTID)
        self.assertEqual(0,await restrictFunctions.getRestrictScheduleNum(TESTID))

if __name__ == '__main__':
    unittest.main()