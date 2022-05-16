from unittest import IsolatedAsyncioTestCase
import unittest
import rulesFunctions

TESTID = 1 #Going under assumption that no discord server has guild id of TESTID
EXPECTEDRULES = 1

class RulesTests(IsolatedAsyncioTestCase):

    def test(self):
        self.assertTrue(True)

    async def test_addRules(self):
        self.assertEqual("Rule added: TEST RULE",await rulesFunctions.addRuleCommand(TESTID,"TEST RULE"))
        self.assertEqual("Rule already exists: TEST RULE",await rulesFunctions.addRuleCommand(TESTID,"TEST RULE"))
        await rulesFunctions.clearRulesCommand(TESTID)

    async def test_getRules(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        self.assertEqual("NO RULES CURRENTLY",await rulesFunctions.getRulesCommand(TESTID))
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE")
        self.assertEqual("RULES\n1. TEST RULE \n",await rulesFunctions.getRulesCommand(TESTID))
        await rulesFunctions.clearRulesCommand(TESTID)
        
    async def test_clearRules(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE")
        self.assertEqual(EXPECTEDRULES,await rulesFunctions.getNumRulesCommand(TESTID))
        await rulesFunctions.clearRulesCommand(TESTID)
        self.assertEqual(0,await rulesFunctions.getNumRulesCommand(TESTID))
        

    async def test_numRules(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        self.assertEqual(0,await rulesFunctions.getNumRulesCommand(TESTID))
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE")
        self.assertEqual(1,await rulesFunctions.getNumRulesCommand(TESTID))
        await rulesFunctions.clearRulesCommand(TESTID)

if __name__ == '__main__':
    unittest.main()