import unittest
import aiosqlite
import listsFunctions
import tables

DBFILE = "main.db"
TESTID = 1

class ListsTests(unittest.IsolatedAsyncioTestCase):

    async def check_db_entry(self, guild_id, name, post_id):
        await tables.create_tables()
        async with aiosqlite.connect(DBFILE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM listsTable WHERE guild = ? AND name = ? AND postid = ?", (guild_id, name, post_id))
                return await cursor.fetchone()  # access with index: 1 name, 2 postid, 3 note

    def test(self):
        self.assertTrue(True)

    async def test_list_add(self):
        # Clear the db before starting
        await listsFunctions.list_clear(TESTID)
        # Insert into empty db: name='one', note='1st note for one'; should be given postid=1
        await listsFunctions.list_add('one', '1st note for one', TESTID)
        result = await self.check_db_entry(TESTID, 'one', 1)
        self.assertEqual('one', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for one', result[3])
        # Insert into db: name='one', note='2nd note for one'; should be given postid=2
        await listsFunctions.list_add('one', '2nd note for one', TESTID)
        result = await self.check_db_entry(TESTID, 'one', 2)
        self.assertEqual('one', result[1])
        self.assertEqual(2, result[2])
        self.assertEqual('2nd note for one', result[3])
        # Insert into db: name='two', note='1st note for two'; should be given postid=1
        await listsFunctions.list_add('two', '1st note for two', TESTID)
        result = await self.check_db_entry(TESTID, 'two', 1)
        self.assertEqual('two', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for two', result[3])

    async def test_list_edit(self):
        # Clear the db before starting
        await listsFunctions.list_clear(TESTID)
        # Attempt to edit non-existent entry: name='three' postid=1 note='1st note for three'
        self.assertEqual('Unable to find a note with id 1 in list three. Create the note using listadd name note.',
            await listsFunctions.list_edit('three', 1, '1st note for three', TESTID))
        # Add the entry
        await listsFunctions.list_add('three', '1st note for three', TESTID)
        result = await self.check_db_entry(TESTID, 'three', 1)
        self.assertEqual('three', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for three', result[3])
        # Edit the entry
        await listsFunctions.list_edit('three', 1, 'edited 1st note for three', TESTID)
        result = await self.check_db_entry(TESTID, 'three', 1)
        self.assertEqual('three', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('edited 1st note for three', result[3])
    
    async def test_list_remove(self):
        # Clear the db before starting
        await listsFunctions.list_clear(TESTID)
        # Attempt to remove non-existent entry: name='four' postid=1
        self.assertEqual('Did not find post 1 in list: four.',
            await listsFunctions.list_remove('four', 1, TESTID))
        # Add the entry to four
        await listsFunctions.list_add('four', '1st note for four', TESTID)
        result = await self.check_db_entry(TESTID, 'four', 1)
        self.assertEqual('four', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for four', result[3])
        # Remove the entry
        await listsFunctions.list_remove('four', 1, TESTID)
        result = await self.check_db_entry(TESTID, 'four', 1)
        self.assertIsNone(result)
        # Attempt to delete non-existent list: name='five'
        self.assertEqual('Did not find list: five.',
            await listsFunctions.list_remove('five', -1, TESTID))
        # Add the entry to five
        await listsFunctions.list_add('five', '1st note for five', TESTID)
        result = await self.check_db_entry(TESTID, 'five', 1)
        self.assertEqual('five', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for five', result[3])
        # Remove the list
        await listsFunctions.list_remove('five', -1, TESTID)
        result = await self.check_db_entry(TESTID, 'five', 1)
        self.assertIsNone(result)

    async def test_list_clear(self):
        # Clear the db before starting
        await listsFunctions.list_clear(TESTID)
        # Add two lists, 'six' and 'seven'
        await listsFunctions.list_add('six', '1st note for six', TESTID)
        await listsFunctions.list_add('seven', '1st note for seven', TESTID)
        await listsFunctions.list_add('seven', '2nd note for seven', TESTID)
        result = await self.check_db_entry(TESTID, 'six', 1)
        self.assertEqual('six', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for six', result[3])
        result = await self.check_db_entry(TESTID, 'seven', 1)
        self.assertEqual('seven', result[1])
        self.assertEqual(1, result[2])
        self.assertEqual('1st note for seven', result[3])
        result = await self.check_db_entry(TESTID, 'seven', 2)
        self.assertEqual('seven', result[1])
        self.assertEqual(2, result[2])
        self.assertEqual('2nd note for seven', result[3])
        # Clear the list
        await listsFunctions.list_clear(TESTID)
        result = await self.check_db_entry(TESTID, 'six', 1)
        self.assertIsNone(result)
        result = await self.check_db_entry(TESTID, 'seven', 1)
        self.assertIsNone(result)
        result = await self.check_db_entry(TESTID, 'seven', 1)
        self.assertIsNone(result)


    async def test_list_check(self):
        # Clear the db before starting
        await listsFunctions.list_clear(TESTID)
        # Check the empty db
        self.assertEqual('No lists found.',
            await listsFunctions.list_check('', TESTID))
        # Add a post to list 'eight'
        await listsFunctions.list_add('eight', '1st note for eight', TESTID)
        # Check list 'eight'
        self.assertEqual('**Showing List: eight**\n1) 1st note for eight\n',
            await listsFunctions.list_check('eight', TESTID))
        # Edit the post
        await listsFunctions.list_edit('eight', 1, 'edited 1st note for eight', TESTID)
        # Check list 'eight' again
        self.assertEqual('**Showing List: eight**\n1) edited 1st note for eight\n',
            await listsFunctions.list_check('eight', TESTID))
        # Add another post to list 'eight'
        await listsFunctions.list_add('eight', '2nd note for eight', TESTID)
        # Check list 'eight' again
        self.assertEqual('**Showing List: eight**\n1) edited 1st note for eight\n2) 2nd note for eight\n',
            await listsFunctions.list_check('eight', TESTID))
        # Add a post to list 'nine'
        await listsFunctions.list_add('nine', '1st note for nine', TESTID)
        # Check list 'nine'
        self.assertEqual('**Showing List: nine**\n1) 1st note for nine\n',
            await listsFunctions.list_check('nine', TESTID))
        # Check all lists
        self.assertEqual('**Showing All Lists**\n__List: eight__\n1) edited 1st note for eight\n2) 2nd note for eight\n__List: nine__\n1) 1st note for nine\n',
            await listsFunctions.list_check('', TESTID))
        # Delete the only post from list 'nine'
        await listsFunctions.list_remove('nine', 1, TESTID)
        # Check non-existent list 'nine'
        self.assertEqual('Could not find notes in list: nine',
            await listsFunctions.list_check('nine', TESTID))
        # Check all lists
        self.assertEqual('**Showing All Lists**\n__List: eight__\n1) edited 1st note for eight\n2) 2nd note for eight\n',
            await listsFunctions.list_check('', TESTID))
        # Clear all lists
        await listsFunctions.list_clear(TESTID)
        # Check all lists
        self.assertEqual('No lists found.',
            await listsFunctions.list_check('', TESTID))

if __name__=='__main__':
    unittest.main()