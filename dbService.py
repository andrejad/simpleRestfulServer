# This script:
# 1) Creates the DB "datastore" and a table "dataT" (with default dataset) upon startup, if they don't exist. 
# 2) Provides a set of insert/edit/read/delete methods for dataT table.

import sqlite3
import json

dbName = "datastore"

# Creates the database dnBame (if doesn't exist), table dataT, and inserting initial data.
def initTableDataT():

    # tabe "dataT" has the follwing columns:
    # rowid(int) - Primary key. Automatically inserted. Not editable or insertable by user.     
    # timestamp(text) DEFAULT (datetime('now','localtime')) - Automatically inserted. Not editable or insertable by user.
    # owner(text) - Can be used to identify the sender of a record. Various sensors can have their unique Owner id's.
    # priority(int) - Can be used to classify the type of message (temperature, speed, etc) or to determine the priority.
    # message(text) - The data itself
    #
    createDataT = "CREATE TABLE IF NOT EXISTS dataT (timestamp text DEFAULT CURRENT_TIMESTAMP, owner text, priority int, message text)"

    # Dafault data to be loaded if the table dataT doesn't exist. Small dataset for testing.
    #
    defData = [["ana", 1, "note no.1"], ["bob", 1, "note #2"], ["carl", 2, "note #3"], ["dave", 1, "note #4"]]
    
    # If dataT doens't exist it will be created and small dataset will be iserted.
    #
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute(createDataT) # Create table dataT if it doesn't exist.
    con.commit()
    res = cur.execute("select count(*) from dataT").fetchone() # Is the table empty?
    if res[0] == 0: # If the table is empty, insert small dataset.
        for defRow in defData:
            cur.execute("insert into dataT (owner, priority, message) values (?,?,?)", defRow)
    con.commit()
    # Check how many rows are in the table
    res = cur.execute("select count(*) from dataT").fetchone() 
    con.close()
    print ("Number of rows in dataT table:", res[0])

# Fetching all rows from the table (limited amount of rows as parameter, absolute limit=100)
def getAllDataT(lim):
    
    if lim > 100:
        print("getAllDataT absolute limit 100 rows")
        lim = 100
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    limit = "" if lim == 0 else " limit " + str(lim)
    cur.execute("select rowid, * from dataT order by rowid desc " + limit)
    d = []
    while True:
        row = cur.fetchone()
        if row == None:
            break
        d.append(row)
    # print("json.dumps(getAllDataT)", json.dumps(d)) # For debugging/logging purposes.
    con.close()
    return d

# Fetching all records from the table by owner. Amount of rows as lim(it) parameter (absolute max limit=100).
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
    con.close()
    # print("json.dumps(getAllByOwner)", json.dumps(d)) # For debugging/logging purposes.
    return d

# Inserting new record. Timestamp and rowid (PK) are insterted automatically.
def putNewTask(owner, priority, message):
    
    print ("db put new taks")
    # TODO: validation parameters
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    cur.execute("insert into dataT (owner, priority, message) values (?,?,?)", (owner,  int(priority), message))
    con.commit()
    con.close()
    return {'status': 'ok'}

# Updating a record, identified by rowid (primary key).
def updateDataT(rowid, owner, priority, message):
    
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    # TODO: Validation if rowid exists, and return a propriate errorcode.
    cur.execute("UPDATE dataT SET owner = ?, priority = ?, message = ? WHERE rowid=?", (owner, int(priority), message, rowid))
    con.commit()
    con.close()
    return {'status': 'ok'}

# Deleting a record, identified by rowid (primary key)
def deleteTask(rowid):
    
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    # TODO: Validation if rowid exists, and return a propriate errorcode.
    cur.execute("delete from dataT where rowid=?", (rowid,))
    con.commit()
    con.close()
    return {'status': 'ok'}

# Fetching a record based on a rowid (PK).
def getById(rowid):
    
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    # TODO: Validation if rowid exists, and return a propriate errorcode.
    cur.execute("select rowid, * from dataT where rowid=?", (rowid,))
    d = [cur.fetchone()]    
    con.close()
    return d

# Internal method for transforming the data into a list (dictionary).
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
    # print("retList", retList) # For debugging/logging purposes.
    return retList

# Following calls will be executed on startup in order to create DB and table if they don't exist,
# and to display the count of data in the dataT table.
#
# Create table if not already created
initTableDataT()
#
# Read from table, for testing purposes.
getAllDataT(100)
