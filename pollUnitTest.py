from unittest import IsolatedAsyncioTestCase
import unittest
import pollFunctions

EMPTY = 0
MAX_OPTIONS = 10

DEFAULT_VALID = 1
ERROR_NUM_VOTES_ZERO = -1
ERROR_OPTIONS_VOTE_MISMATCH = -2
ERROR_EXCEED_MAX_VOTES = -3

class SchedulePollTests(IsolatedAsyncioTestCase):

    def test(self):
        self.assertTrue(True)

    def test_displayIntroPage(self):   
        self.assertTrue(pollFunctions.displayIntroPage())

    def test_checkIfValid(self):
        self.assertEqual(DEFAULT_VALID,pollFunctions.checkIfValid(8,8))
        self.assertEqual(DEFAULT_VALID,pollFunctions.checkIfValid(1,1))
        self.assertEqual(ERROR_NUM_VOTES_ZERO,pollFunctions.checkIfValid(0,1000))
        self.assertEqual(ERROR_NUM_VOTES_ZERO,pollFunctions.checkIfValid(-5,-6))
        self.assertEqual(ERROR_OPTIONS_VOTE_MISMATCH,pollFunctions.checkIfValid(5,-6))
        self.assertEqual(ERROR_OPTIONS_VOTE_MISMATCH,pollFunctions.checkIfValid(50,60))
        self.assertEqual(ERROR_EXCEED_MAX_VOTES,pollFunctions.checkIfValid(11,11))
        self.assertEqual(ERROR_EXCEED_MAX_VOTES,pollFunctions.checkIfValid(10000,10000))
    
    def test_displayIntroPage(self):   
        self.assertTrue(pollFunctions.displayPoll("test1", "a"))
        self.assertTrue(pollFunctions.displayPoll("test2", ["aa","bb","cc"]))        
        
if __name__ == '__main__':
    unittest.main()