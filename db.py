import sqlite3
from datetime import datetime, date

# [operation] [to: user] [on: table] [option]
operations = ['grant', 'forbid', 'print', 'access']
options = ['grantable']

# table list that only SO can access
so_access_only_tables = ['forbidden', 'assigned', 'dblog']

# Start DB
def startDB():
    global conn, cur
    conn = sqlite3.connect(':memory:')
    # Query result will return as dictionary
    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    cur = conn.cursor()

# Close DB
def closeDB():
    conn.close()

# Create user table
def createUserTable():
    cur.execute("CREATE TABLE users (id integer primary key, user_name text, user_type text)")
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('admin', 'so')")
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('marek', 'reg')")
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('dexter', 'reg')")
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('tester', 'reg')")
    conn.commit()

# Create 'assigned', 'forbidden', 'dblog' table
def createSystemTables():
    cur.execute("CREATE TABLE assigned (id integer primary key, user_name text, table_name text, grantable integer, forbid_attempt integer)")
    cur.execute("CREATE TABLE forbidden (id integer primary key, user_name text, table_name text)")
    cur.execute("CREATE TABLE dblog (id integer primary key, log_type text, log_msg text, [timestamp] timestamp)")
    conn.commit()

    # By default, regular users can access to emp table
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt) VALUES ('marek', 'emp', 1, 0)")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt) VALUES ('dexter', 'emp', 0, 0)")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt) VALUES ('tester', 'emp', 0, 0)")

    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt) VALUES ('marek', 'reglog', 0, 0)")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt) VALUES ('dexter', 'reglog', 0, 0)")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt) VALUES ('tester', 'reglog', 0, 0)")
    conn.commit()

# Populate sample data that regular user can access
def createRegularTables():
    # reglog is log table for regular users (warnings to each users)
    cur.execute("CREATE TABLE reglog(id integer primary key, to_user_name text, log_msg text, [timestamp] timestamp)")

    cur.execute("CREATE TABLE emp (emp_id text, emp_name text)")
    cur.execute("INSERT INTO emp(emp_id, emp_name) VALUES ('1', 'Marek')")
    cur.execute("INSERT INTO emp(emp_id, emp_name) VALUES ('2', 'Dexter')")
    cur.execute("INSERT INTO emp(emp_id, emp_name) VALUES ('3', 'Tester')")

    cur.execute("CREATE TABLE salary (emp_id text, emp_salary real)")
    cur.execute("INSERT INTO salary(emp_id, emp_salary) VALUES ('1', 95000)")
    cur.execute("INSERT INTO salary(emp_id, emp_salary) VALUES ('2', 70000)")
    cur.execute("INSERT INTO salary(emp_id, emp_salary) VALUES ('3', 35000)")
    conn.commit()


# Query user table with user name
def queryUser(targetUserName):
    cur.execute("SELECT user_name, user_type FROM users WHERE user_name=?", [targetUserName])
    queryResult = cur.fetchone()
    return queryResult

# Check if user name exists in user table and return true if user exists
def tryToLoginUser(targetUserName):
    queryResult = queryUser(targetUserName)
    isUserSO = False
    if queryResult:
        if queryResult["user_type"] == 'so':
            print('Welcome [' + queryResult["user_name"]  + ']: You are Security Officer')
            isUserSO = True
        else:
            print('Welcome [' + queryResult["user_name"] + ']: You are regular user')
            isUserSO = False
        return True, isUserSO
    else:
        return False, False


# Check if table exists
def checkIfTableExist(targetTableName):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [targetTableName])
    queryResult = cur.fetchone()
    return queryResult

# Check if requested query is valid or not
def checkValidQuery(query):
    # Parse query
    strArr = query.split()
    strArrLen = len(strArr)

    # Check if the query is at least 3
    if strArrLen < 2:
        print ('Invalid query! Query needs to be at least 2 parts')
        return False

    # First part needs to be proper operation command
    operation = strArr[0].lower()
    if operation.strip() not in operations:
        print('Invalid operation! List of operations:')
        print(operations)
        return False

    # Handle print operation
    if strArrLen == 2:
        if operation == 'print' or operation == 'access':
            targetTable = strArr[1]
            queryResult = checkIfTableExist(targetTable)
            if queryResult == None:
                print('Target table is not in database!')
                return False
        return True

    # Second part is target user
    targetUserName = strArr[1]
    queryResult = queryUser(targetUserName)
    if queryResult == None:
        print('Target user is not in database!')
        return False

    # Third part is target table
    targetTable = strArr[2]
    queryResult = checkIfTableExist(targetTable)
    if queryResult == None:
        print('Target table is not in database!')
        return False

    # Fourth part is option
    if len(strArr) == 4:
        option = strArr[3].lower()
        if option.strip() not in options:
            print('Invalid option! List of options:')
            print(options)
            return False
    return True

# Log important message into dblog table
def logMessage(logType, message):
    # Insert log message
    cur.execute("INSERT INTO dblog(log_type, log_msg, timestamp) VALUES (?, ?, ?)", (logType, message, datetime.now()))
    conn.commit()

# List all rows for target table
def printTable(userName, isUserSO, targetTableName):
    # First, check if the user has privilege
    if accessTable(userName, isUserSO, targetTableName):
        cur.execute("SELECT * FROM {}".format(targetTableName))
        queryResult = cur.fetchall()
        for row in queryResult:
            print(row)

# Access table
def accessTable(userName, isUserSO, targetTableName):
    # Check if regular user is trying to access SO only accessable tables
    if targetTableName in so_access_only_tables:
        if isUserSO == False:
            print('You have no access to this table [' + targetTableName + ']')
            logMessage('ERROR', 'Invalid access attempt from [' + userName + '] to table [' + targetTableName +']')
            return False
    return True

# Grant access to another user
def grantAccess(userName, isUserSO, targetUser, targetTable, grantable):
    # Insert into assigned table
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable) VALUES (?, ?, ?)", (targetUser, targetTable, grantable))
    conn.commit()
    return True

# Add user into forbidden table
def addUserToForbiddenTable(targetUser, targetTable):
    print('User [' + targetUser + '] added on forbid list')
    cur.execute("INSERT INTO forbidden(user_name, table_name) VALUES (?, ?)", (targetUser, targetTable))
    conn.commit()

# Forbid access of user to target table
def forbidAccess(userName, isUserSO, targetUser, targetTable):
    # Is user security officer?
    if isUserSO == True:
        # Check if target user has access to the target table
        cur.execute("SELECT * FROM assigned WHERE user_name=? AND table_name=?", [targetUser, targetTable])
        queryResult = cur.fetchone()

        # If so, print out warning message (first attempt failed) and update attempt value
        if queryResult != None:
            # Check if forbid attemp was made before and if this is first forbid attempt,
            # stop forbidding operation and add forbid_attempt 1 and notify SO
            if queryResult["forbid_attempt"] == 0:
                print('User [' + targetUser + '] is in assigned table. Try operation again if you want to overwrite.')
                print('Warning: if you overwrite, then it may result disruption of operaionts for delegated users.')
                cur.execute("UPDATE assigned SET forbid_attempt = 1 WHERE user_name=? AND table_name=?", (targetUser, targetTable))
                conn.commit()
            # If this is second forbid attempt, then just remove it from assigned table
            # And add to forbidden table
            elif queryResult["forbid_attempt"] == 1:
                cur.execute("DELETE FROM assigned WHERE user_name=? AND table_name=?", (targetUser, targetTable))
                conn.commit()
                addUserToForbiddenTable(targetUser, targetTable)
        else:
            # Add target user into forbidden table
            addUserToForbiddenTable(targetUser, targetTable)

        # At the same time, warn SO that this will make all delegations revoked [ToDo]
    else:
        print('You do not have privilege to access system table')
        # Regular user tried to write forbidden table => report to SO
        logMessage('ERROR', 'Regular user [' + userName + '] tried to forbid access of [' + targetUser + '] on table [' + targetTable + ']')
        conn.commit()
        return False

# Perform query (validness of query has been checked)
def performQuery(userName, isUserSO, query):
    strArr = query.split()
    operation = strArr[0].lower()

    if operation == 'print':
        printTable(userName, isUserSO, strArr[1])
    elif operation == 'access':
        accessTable(userName, isUserSO, strArr[1])
    elif operation == 'grant':
        targetUser = strArr[1]
        targetTable = strArr[2]
        grantable = False
        if len(strArr) > 3 and strArr[3].lower() == 'grantable':
            grantable = True
        grantAccess(userName, isUserSO, targetUser, targetTable, grantable)
    elif operation == 'forbid':
        targetUser = strArr[1]
        targetTable = strArr[2]
        forbidAccess(userName, isUserSO, targetUser, targetTable)
    else:
        print('invalid operation')
    return True
