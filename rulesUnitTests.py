from unittest import IsolatedAsyncioTestCase
import unittest
import rulesFunctions
import tables
import aiosqlite

DBFILE = "main.db"
TESTID = 1 #Going under assumption that no discord server has guild id of TESTID
EXPECTEDRULES = 1

class RulesTests(IsolatedAsyncioTestCase):

    async def check_db_entry(self, guild_id):
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT rules FROM rulesTable WHERE guild = ?", (guild_id,))
                return await cursor.fetchone()  

    async def test_addRule(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE")
        self.assertEqual("TEST RULE",(await self.check_db_entry(TESTID))[0])
        await rulesFunctions.clearRulesCommand(TESTID)

    async def test_addRuleExist(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        self.assertEqual("Rule added: TEST RULE",await rulesFunctions.addRuleCommand(TESTID,"TEST RULE"))
        self.assertEqual("Rule already exists: TEST RULE",await rulesFunctions.addRuleCommand(TESTID,"TEST RULE"))
        await rulesFunctions.clearRulesCommand(TESTID)

    async def test_getRules(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        self.assertEqual("NO RULES CURRENTLY",await rulesFunctions.getRulesCommand(TESTID))
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE")
        self.assertEqual("RULES\n1. TEST RULE \n",await rulesFunctions.getRulesCommand(TESTID))
        await rulesFunctions.clearRulesCommand(TESTID)
        
    async def test_addMultipleRules(self):
        await rulesFunctions.clearRulesCommand(TESTID)
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE 1")
        await rulesFunctions.addRuleCommand(TESTID,"TEST RULE 2")
        self.assertEqual("RULES\n1. TEST RULE 1 \n2. TEST RULE 2 \n",await rulesFunctions.getRulesCommand(TESTID))
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