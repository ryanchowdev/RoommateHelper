from unittest import IsolatedAsyncioTestCase
import unittest
import helpFunctions

class SchedulehelpTests(IsolatedAsyncioTestCase):

    def test(self):
        self.assertTrue(True)

    def test_displayIntroPage(self):   
        self.assertTrue(helpFunctions.displayIntroPage())

    def test_displayAlarmPage(self):
        self.assertTrue(helpFunctions.displayAlarmPage())
        
    def test_displayCalculatorPage(self):
        self.assertTrue(helpFunctions.displayCalculatorPage())
        
    def test_displayCoinFlipPage(self):
        self.assertTrue(helpFunctions.displayCoinFlipPage())
        
    def test_displayGMapsPage(self):
        self.assertTrue(helpFunctions.displayGMapsPage())
        
    def test_displayMoneyPage(self):
        self.assertTrue(helpFunctions.displayMoneyPage())
        
    def test_displayMusicPage(self):
        self.assertTrue(helpFunctions.displayMusicPage())
        
    def test_displayPollPage(self):
        self.assertTrue(helpFunctions.displayPollPage())
        
    def test_displayRestrictPage(self):
        self.assertTrue(helpFunctions.displayRestrictPage())
        
    def test_displayRulesPage(self):
        self.assertTrue(helpFunctions.displayRulesPage())
        
    def test_displaySchedulePage(self):
        self.assertTrue(helpFunctions.displaySchedulePage())
        
    def test_displayWeatherPage(self):
        self.assertTrue(helpFunctions.displayWeatherPage())
        
    def test_displayListsPage(self):
        self.assertTrue(helpFunctions.displayListsPage())
        
if __name__ == '__main__':
    unittest.main()