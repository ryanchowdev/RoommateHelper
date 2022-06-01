import aiosqlite
from datetime import datetime , date, timedelta 
import random

ERRORNUM = -1
DATEFORMAT = "%Y-%m-%d %H:%M:%S"
OTHERDATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"
RANDSTART = 100000000
RANDEND = 999999999

CTXList = []

# Adds current ctx to active list
def addToActive(ctx):
    check = False
    for i in range(0, len(CTXList)):
        if ctx.guild.id == CTXList[i].guild.id:
            check = True
    if not check:
        CTXList.append(ctx)

# Returns ctx list
def getCTXList():
    return CTXList.copy()

# removes ctx from ctx list
def removeFromActive(ctx):
    for i in range(0,len(CTXList)):
        if ctx.guild.id == CTXList[i].guild.id:
            CTXList.pop(i)
            break

# converts command to minutes
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

# Returns the date in which scheduler is configured to be (current time/future time)
def dateConversion(dateStart:str):
    currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
    if dateStart !="":
        try:
            assignedTime = datetime.strptime(dateStart, "%m/%d/%Y %H:%M")
            if assignedTime < currentTime:
                return ERRORNUM
            currentTime = assignedTime
        except:
            return ERRORNUM
    return currentTime

# Insert the parameters into the database
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

# Repeat past time until current time based on the time between given
async def repeatUntilPresentFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchall()
            if data:
                currentTime = datetime.strptime(datetime.now().strftime("%Y-%m-%d, %H:%M"),"%Y-%m-%d, %H:%M")
                expectedTime = currentTime
                for d in data:
                    d = list(d)
                    try:
                        expectedTime = datetime.strptime(d[2],DATEFORMAT)
                    except:
                        expectedTime = datetime.strptime(d[2],OTHERDATEFORMAT)
                    timeDiff = int((expectedTime-currentTime).total_seconds())/60
                    if int((expectedTime-currentTime).total_seconds() / 60)<=0:
                        timeDiff = abs(timeDiff)
                        num = timeDiff/d[1]
                        if timeDiff % d[1]>0:
                            num+=1
                        expectedTime = expectedTime+timedelta(minutes=(d[1]*(num)))
                    d[2] = expectedTime
                    await cursor.execute("UPDATE schedulesTable SET alarmTime = ? WHERE guild = ? AND id = ?",(d[2],d[0],d[6]))
                await db.commit()
                return True
    return False

# Deletes from db based on scheduling id and server id
async def deleteScheduleFunction(Gid,id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM schedulesTable WHERE guild = ? AND id = ?",(Gid,id))
        await db.commit()
    return "DELETED SCHEDULE"

# Deletes from db based on server id
async def clearScheduleFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("DELETE FROM schedulesTable WHERE guild = ?",(id,))
        await db.commit()
    return "CLEARED SCHEDULES"
                
# Returns all current schedules
async def getScheduleFunction(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * from schedulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchall()
            if data:
                string = "SCHEDULES\n"
                for i in data:
                    string += f"Message: {(i[4])} Next Time: {i[2][0:16]} ID: {i[6]}\n"
                return string
            else:
                return "No Schedules Currently"

# Returns the amount of schedules for the server
async def getScheduleNum(id):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT COUNT(*) FROM schedulesTable WHERE guild = ?",(id,))
            data = await cursor.fetchone()
        await db.commit()
    return data[0]