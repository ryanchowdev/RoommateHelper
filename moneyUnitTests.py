import unittest
import aiosqlite
import moneyFunctions
import tables

DBFILE = "main.db"
TESTID = 1

class MoneyTests(unittest.IsolatedAsyncioTestCase):

    async def check_db_entry(self, guild_id, name):
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM moneyTable WHERE guild = ? AND person = ?", (guild_id, name))
                return await cursor.fetchone()  # access with index: 1 person, 2 amount, 3 reason

    def test(self):
        self.assertTrue(True)

    async def test_set_debt(self):
        # Clear the db before starting
        await moneyFunctions.clear_debt(TESTID)
        # Insert into db: person='one', amount=1, reason='test inserted 1'
        await moneyFunctions.set_debt('one', 1, 'test inserted 1', TESTID)
        result = await self.check_db_entry(TESTID, 'one')
        self.assertEqual('one', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('test inserted 1', result[3])
        # Insert into db: person='two', amount=5.55, reason='None'
        await moneyFunctions.set_debt('two', 5.55, None, TESTID)
        result = await self.check_db_entry(TESTID, 'two')
        self.assertEqual('two', result[1])
        self.assertEqual(5.55, result[2])
        self.assertEqual(None, result[3])

    async def test_change_debt(self):
        # Clear the db before starting
        await moneyFunctions.clear_debt(TESTID)
        # Change entry in db: person='three', amount=30.5
        # This will insert a new entry in the db since it does not exist
        await moneyFunctions.change_debt('three', 30.5, TESTID)
        result = await self.check_db_entry(TESTID, 'three')
        self.assertEqual('three', result[1])
        self.assertEqual(30.5, result[2])
        self.assertEqual(None, result[3])
        # Change entry for 'three' to: amount += 10
        # Increments the amount
        await moneyFunctions.change_debt('three', 10, TESTID)
        result = await self.check_db_entry(TESTID, 'three')
        self.assertEqual('three', result[1])
        self.assertEqual(40.5, result[2])
        self.assertEqual(None, result[3])
        # Change entry for 'three' to: amount -= 25
        # Decrements the amount
        await moneyFunctions.change_debt('three', -25, TESTID)
        result = await self.check_db_entry(TESTID, 'three')
        self.assertEqual('three', result[1])
        self.assertEqual(15.5, result[2])
        self.assertEqual(None, result[3])
        # Change entry for 'three' to: amount -= 100
        # Decrements the amount below 0, so it should be set to 0
        await moneyFunctions.change_debt('three', -100, TESTID)
        result = await self.check_db_entry(TESTID, 'three')
        self.assertEqual('three', result[1])
        self.assertEqual(0, result[2])
        self.assertEqual(None, result[3])

    async def test_change_note(self):
        # Clear the db before starting
        await moneyFunctions.clear_debt(TESTID)
        # Change note in db: person='four', reason='Hello World!'
        # This will insert a new entry in the db since it does not exist
        await moneyFunctions.change_note('four', 'Hello World!', TESTID)
        result = await self.check_db_entry(TESTID, 'four')
        self.assertEqual('four', result[1])
        self.assertEqual(0, result[2])
        self.assertEqual('Hello World!', result[3])
        # Change entry for 'four' to: note = 'Ciao Mondo!'
        # Changes note for existing entry
        await moneyFunctions.change_note('four', 'Ciao Mondo!', TESTID)
        result = await self.check_db_entry(TESTID, 'four')
        self.assertEqual('four', result[1])
        self.assertEqual(0, result[2])
        self.assertEqual('Ciao Mondo!', result[3])
        # Change entry for 'four' to: None
        # If no argument is provided to the bot, the default note would be None
        await moneyFunctions.change_note('four', None, TESTID)
        result = await self.check_db_entry(TESTID, 'four')
        self.assertEqual('four', result[1])
        self.assertEqual(0, result[2])
        self.assertEqual(None, result[3])

    async def test_check_debt(self):
        # Clear the db before starting
        await moneyFunctions.clear_debt(TESTID)
        # Check empty db
        self.assertEqual('No current debts.', await moneyFunctions.check_debt(TESTID))
        # Add one entry
        await moneyFunctions.set_debt('five', 21.99, 'test user 5', TESTID)
        self.assertEqual('**Current Debts**\nfive owes $21.99. Note: test user 5\n',
                        await moneyFunctions.check_debt(TESTID))
        # Add another entry
        await moneyFunctions.set_debt('six', 93, None, TESTID)
        self.assertEqual('**Current Debts**\nfive owes $21.99. Note: test user 5\nsix owes $93.0. Note: None\n',
                        await moneyFunctions.check_debt(TESTID))
        # Edit an entry amount
        await moneyFunctions.change_debt('six', -50, TESTID)
        self.assertEqual('**Current Debts**\nfive owes $21.99. Note: test user 5\nsix owes $43.0. Note: None\n',
                        await moneyFunctions.check_debt(TESTID))
        # Edit an entry note
        await moneyFunctions.change_note('six', 'test user 6', TESTID)
        self.assertEqual('**Current Debts**\nfive owes $21.99. Note: test user 5\nsix owes $43.0. Note: test user 6\n',
                        await moneyFunctions.check_debt(TESTID))
        # Clear db
        await moneyFunctions.clear_debt(TESTID)
        self.assertEqual('No current debts.', await moneyFunctions.check_debt(TESTID))

    async def test_clear_debt(self):
        # Clear the db
        await moneyFunctions.clear_debt(TESTID)
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM moneyTable WHERE guild = ?", (TESTID,))
                # Check db for TESTID is empty
                self.assertEqual(None, await cursor.fetchone())
                # Add entry to db
                await moneyFunctions.set_debt('seven', 7.77, 'inserted user 7', TESTID)
                result = await self.check_db_entry(TESTID, 'seven')
                self.assertEqual('seven', result[1])
                self.assertEqual(7.77, result[2])
                self.assertEqual('inserted user 7', result[3])
                # Add another entry to db
                await moneyFunctions.set_debt('eight', 8.88, 'inserted user 8', TESTID)
                result = await self.check_db_entry(TESTID, 'eight')
                self.assertEqual('eight', result[1])
                self.assertEqual(8.88, result[2])
                self.assertEqual('inserted user 8', result[3])
                # Clear the db
                await moneyFunctions.clear_debt(TESTID)
                self.assertEqual(None, await cursor.fetchone())

    async def test_remove_debt(self):
        # Clear the db
        await moneyFunctions.clear_debt(TESTID)
        # Try to remove a non-existent entry in the db
        self.assertEqual('nine did not have any debt.', await moneyFunctions.remove_debt('nine', TESTID))
        # Add an entry
        await moneyFunctions.set_debt('nine', 9.99, 'Bonjour', TESTID)
        result = await self.check_db_entry(TESTID, 'nine')
        self.assertEqual('nine', result[1])
        self.assertEqual(9.99, result[2])
        self.assertEqual('Bonjour', result[3])
        # Remove the entry
        self.assertEqual('Removed debt for nine.', await moneyFunctions.remove_debt('nine', TESTID))
        self.assertEqual(None, await self.check_db_entry(TESTID, 'nine'))

if __name__=='__main__':
    unittest.main()