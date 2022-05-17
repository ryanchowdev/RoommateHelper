import aiosqlite
from datetime import datetime , date, timedelta 
import random

ERRORNUM = -1
DATEFORMAT = "%Y-%m-%d %H:%M:%S"
OTHERDATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"
RANDSTART = 100000000
RANDEND = 999999999

def convertToMinutes(paramOne:str ,paramTwo:int):
    time = paramTwo
    if paramOne in ["m","minute","min"]:
        paramOne = "minute"
    elif paramOne in ["h","hour"]:
        paramOne = "hour"
        time*=60
    elif paramOne in ["d","day"]:
        paramOne = "day"
        time*=60*24
    elif paramOne in ["week","w"]:
        paramOne = "week"
        time*=60*24*7
    elif paramOne in ["year","y"]:
        paramOne = "year"
        time*=60*24*365
    else:
        time = ERRORNUM
    return time

def dateConversion(dateStart:str):
    currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
    if dateStart !="":
        try:
            assignedTime = datetime.strptime(dateStart, "%m/%d/%Y %H:%M")
            if assignedTime < currentTime:
                print("GIVEN TIME TOO LOW")
                return ERRORNUM
        except:
            print("INCORRECT FORMAT")
            return ERRORNUM
    return currentTime

async def insertScheduler(id,time,finalTime,paramOne:str ,paramTwo:int, message:str,stringList:str = ""):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            code = random.randint(RANDSTART,RANDEND)
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ? AND id = ?",(id,code))
            data = await cursor.fetchone()
            while data:
                code = random.randint(RANDSTART,RANDEND)
                await cursor.execute("SELECT * from schedulesTable WHERE guild = ? AND id = ?",(id,code))
                data = await cursor.fetchone()
            await cursor.execute("INSERT INTO schedulesTable (guild,timeBetween,alarmTime,message,list,currentIndex,id) VALUES (?,?,?,?,?,?,?)",(id,time,finalTime,message,stringList,0,code))
            await db.commit()
    return "Scheduled a message every "+ str(paramTwo)+" "+paramOne+" Message: " + message

async def repeatUntilPresentFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchall()
            if data:
                currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
                for d in data:
                    d = list(d)
                    try:
                        expectedTime = datetime.strptime(d[2],DATEFORMAT)
                    except:
                        expectedTime = datetime.strptime(d[2],OTHERDATEFORMAT)
                    while int((expectedTime-currentTime).total_seconds() / 60)<=0:
                        expectedTime = currentTime+timedelta(minutes=d[1])
                    d[2] = expectedTime
                    d = tuple(d)
                return True
    return False

async def deleteScheduleFunction(Gid,id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM schedulesTable WHERE guild = ? AND id = ?",(Gid,id))
        await db.commit()
    return "DELETED SCHEDULE"

async def clearScheduleFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM schedulesTable WHERE guild = ?",(id,))
        await db.commit()
    return "CLEARED SCHEDULES"
                
async def getScheduleFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchall()
            if data:
                string = "SCHEDULES\n"
                for i in data:
                    print(i)
                    string += f"{(i[4])} at {i[2]} id is {i[6]}\n"
                return string
            else:
                return "NO Schedules CURRENTLY"

async def getScheduleNum(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM schedulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchone()
        await db.commit()
    return data[0]