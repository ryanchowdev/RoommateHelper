import unittest
import tables
import asyncio
asyncio.run(tables.create_tables())
loader = unittest.TestLoader()
start_dir = "./"
pattern = "*UnitTest.py"
suite = loader.discover(start_dir, pattern)
runner = unittest.TextTestRunner()
runner.run(suite)
