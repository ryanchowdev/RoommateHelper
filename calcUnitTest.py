from unittest import IsolatedAsyncioTestCase
import unittest
import calcFunctions

VALID = 0
NOINPUT = -1
HASLETTERS = -2

class ScheduleCalcTests(IsolatedAsyncioTestCase):

    def test(self):
        self.assertTrue(True)

    def test_checkValidInput(self):
        self.assertEqual(VALID, calcFunctions.checkValidInput("1+2+3"))
        self.assertEqual(VALID, calcFunctions.checkValidInput("25+*"))
        self.assertEqual(VALID, calcFunctions.checkValidInput("3/0"))
        self.assertEqual(NOINPUT, calcFunctions.checkValidInput(""))
        self.assertEqual(HASLETTERS, calcFunctions.checkValidInput("abc"))
        self.assertEqual(HASLETTERS, calcFunctions.checkValidInput("3x + 45"))
        
    def test_calculate(self):
        self.assertEqual(12,calcFunctions.calculate("7+5"))
        self.assertEqual(3401,calcFunctions.calculate("1+34*100"))
        self.assertEqual(3500,calcFunctions.calculate("(1+34)*100"))
        self.assertEqual(None,calcFunctions.calculate("abc"))
        self.assertEqual(None,calcFunctions.calculate("6/0"))
        
        
if __name__ == '__main__':
    unittest.main()