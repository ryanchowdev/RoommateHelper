from unittest import IsolatedAsyncioTestCase
import unittest
import coinFunctions

class SchedulePollTests(IsolatedAsyncioTestCase):

    def test(self):
        self.assertTrue(True)

    def test_displayHeads(self):   
        self.assertTrue(coinFunctions.displayHeads())
    
    def test_displayTails(self):   
        self.assertTrue(coinFunctions.displayTails())  
        
if __name__ == '__main__':
    unittest.main()