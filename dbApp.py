import sqlite3
import json

dbName = "datastore"

# DEFAULT (datetime('now','localtime'))
# rowid(int)
# timestamp(text)
# owner(text)
# priority(int)
# message(text)
createDataT = "CREATE TABLE IF NOT EXISTS dataT (timestamp text DEFAULT CURRENT_TIMESTAMP, owner text, priority int, message text)"

defData = [["ana", 1, "note no.1"], ["bob", 1, "note #2"], ["carl", 2, "note #3"], ["dave", 1, "note #4"]]

def initTableDataT():
    print("initTableDataT()")
    # if not exist, create table
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute(createDataT)
    con.commit()
    # if has no rows, insert new data
    res = cur.execute("select count(*) from dataT").fetchone()
    if res[0] == 0:
        for defRow in defData:
            cur.execute("insert into dataT (owner, priority, message) values (?,?,?)", defRow)
    con.commit()
    res = cur.execute("select count(*) from dataT").fetchone()
    con.close()
    print ("Number of rows in dataT table:", res[0])

def getAllDataT(lim):
    print("getAllDataT("+str(lim)+")")
    if lim > 100:
        print("getAllDataT absolute limit 100 rows")
        lim = 100

    con = sqlite3.connect(dbName)
    cur = con.cursor()

    limit = "" if lim == 0 else " limit " + str(lim)
    #print("select rowid, * from dataT" + str(limit))
    cur.execute("select rowid, * from dataT order by rowid desc " + limit)
    d = []
    while True:
        row = cur.fetchone()
        if row == None:
            break
        d.append(row)
    #print ("d=",d)
    #print("json.dumps(d)", json.dumps(d))
    con.close()
    return d

def getAllByOwner(owner, lim):
    if lim > 100:
        print("getAllDataT absolute limit 100 rows")
        lim = 100

    con = sqlite3.connect(dbName)
    cur = con.cursor()

    limit = "" if lim == 0 else " limit " + str(lim)
    cur.execute("select rowid, * from dataT where owner=?" + limit + " order by rowid desc", (owner,))
    d = []
    while True:
        row = cur.fetchone()
        if row == None:
            break
        d.append(row)
    #print("json.dumps(d)", json.dumps(d))
    con.close()
    return d

def putNewTask(owner, priority, message):
    print ("db put new taks")
    # TODO: validation parameters
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute("insert into dataT (owner, priority, message) values (?,?,?)", (owner,  int(priority), message))
    con.commit()
    con.close()
    return {'status': 'ok'}

def updateDataT(rowid, owner, priority, message):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    # TODO: validation if rowid exists
    cur.execute("UPDATE dataT SET owner = ?, priority = ?, message = ? WHERE rowid=?", (owner, int(priority), message, rowid))
    con.commit()
    con.close()
    return {'status': 'ok'}

def deleteTask(rowid):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute("delete from dataT where rowid=?", (rowid,))
    con.commit()
    con.close()
    return {'status': 'ok'}

def getById(rowid):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute("select rowid, * from dataT where rowid=?", (rowid,))
    d = [cur.fetchone()]
    # TODO: validation if none
    con.close()
    return d

def rowsToListDict(rows):
    retList = []
    for row in rows:
        dict = {
            'rowId': row[0],
            'timestamp': row[1],
            'owner': row[2],
            'priority': row[3],
            'message': row[4]
        }
        retList.append(dict)
    #print("retList", retList)
    return retList

initTableDataT()
getAllDataT(3)
