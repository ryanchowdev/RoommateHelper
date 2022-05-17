import aiosqlite

RULELISTSTART = 1

async def addRuleCommand(id,rule):
    s = ""
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT rules from rulesTable WHERE guild = ? AND rules = ?",(id,rule))
            data = await cursor.fetchone()
            if data:
                s = f"Rule already exists: {rule}"
            else:
                await cursor.execute("INSERT INTO rulesTable (rules,guild) VALUES (?,?)",(rule,id))
                s =f"Rule added: {rule}"
        await db.commit()
        return s

async def getRulesCommand(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT rules from rulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchall()
            if data:
                string = "RULES\n"
                num = RULELISTSTART
                for i in data:
                    string += f"{num}. {(i[0])} \n"
                    num+=1
                return string
            else:
                return "NO RULES CURRENTLY"

async def clearRulesCommand(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM rulesTable WHERE guild = ?",(id,))
        await db.commit()

async def getNumRulesCommand(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM rulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchone()
        await db.commit()
        return data[0]