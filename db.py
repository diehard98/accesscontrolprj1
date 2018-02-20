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
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('boxter', 'reg')")
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('tester', 'reg')")
    cur.execute("INSERT INTO users(user_name, user_type) VALUES ('worker', 'reg')")
    conn.commit()

# Create 'assigned', 'forbidden', 'dblog' table
def createSystemTables():
    cur.execute("""CREATE TABLE assigned (
                id integer primary key,
                user_name text,
                table_name text,
                grantable integer,
                forbid_attempt integer,
                granted_by text
                )""")
    cur.execute("CREATE TABLE forbidden (id integer primary key, user_name text, table_name text)")
    cur.execute("CREATE TABLE dblog (id integer primary key, log_type text, log_msg text, [timestamp] timestamp)")
    conn.commit()

# Establish database with pre-defined data to test cases
def establishSampleCase():
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('marek', 'salary', 1, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('dexter', 'salary', 1, 0, 'marek')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('boxter', 'salary', 1, 0, 'marek')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('boxter', 'salary', 1, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('tester', 'salary', 0, 0, 'dexter')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('worker', 'salary', 0, 0, 'boxter')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('admin', 'assigned', 0, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('admin', 'forbidden', 0, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('admin', 'dblog', 0, 0, 'admin')")

    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('marek', 'reglog', 0, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('dexter', 'reglog', 0, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('tester', 'reglog', 0, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('boxter', 'reglog', 0, 0, 'admin')")
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES ('worker', 'reglog', 0, 0, 'admin')")
    conn.commit()

# Populate sample data that regular user can access
def createRegularTables():
    # reglog is log table for regular users (warnings to each users)
    cur.execute("CREATE TABLE reglog(id integer primary key, to_user_name text, log_type text, log_msg text, [timestamp] timestamp)")

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

# Log important messages into dblog table (only for security officer)
def logMessageForSO(logType, message):
    cur.execute("INSERT INTO dblog(log_type, log_msg, timestamp) VALUES (?, ?, ?)", (logType, message, datetime.now()))
    conn.commit()

# Log messages into reglog table for all regular users
def logMessageForRegularUsers(toUserName, logType, message):
    cur.execute("INSERT INTO reglog(to_user_name, log_type, log_msg, timestamp) VALUES (?, ?, ?, ?)", (toUserName, logType, message, datetime.now()))
    conn.commit()

# List all rows for target table
def printTable(userName, isUserSO, targetTableName):
    # First, check if the user has privilege
    if accessTable(userName, isUserSO, targetTableName):
        if targetTableName == 'reglog':
            cur.execute("SELECT * FROM reglog WHERE to_user_name=?", [userName])
        else:
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
            logMessageForSO('ERROR', 'Invalid access attempt from [' + userName + '] to table [' + targetTableName +']')
            return False

    # Check if user has access to table
    if not canAccess(userName, targetTableName):
        print('You have no access to this table [' + targetTableName + ']')
        logMessageForSO('ERROR', 'Invalid access attempt from [' + userName + '] to table [' + targetTableName +']')
        return False
    return True

# Grant access to another user
def grantAccess(userName, isUserSO, targetUser, targetTable, grantable):
    # Check if the grant already exist in the assigned table
    cur.execute("SELECT * FROM assigned WHERE user_name=? AND table_name=? AND grantable=? AND granted_by=?", [targetUser, targetTable, grantable, userName])
    queryResult = cur.fetchone()
    if queryResult != None:
        # Same grant exist in the assigned table, so this grant operation will not need to be happened
        print('ERROR: user [' + targetUser + '] already granted access from you on the table [' + targetTable + ']')
        logMessageForSO('Duplicated Grant Operation', 'User [' + userName + '] tried to grant duplicated access to table [' + targetTable +'] on user [' + targetUser + ']')
        return False

    # Check if target user is on the forbidden table by SO
    cur.execute("SELECT * FROM forbidden WHERE user_name=? AND table_name=?", [targetUser, targetTable])
    queryResult = cur.fetchone()
    if queryResult != None:
        # The target user is on the forbidden table which needs to be reported to user who requested and also SO
        logMessageForSO('Dangerous Grant Operation', 'User [' + userName + '] tried to grant access to user [' + targetUser + '] who is forbidden for the table [' + targetTable + ']')
        logMessageForRegularUsers(userName, 'Dangerous Grant Operation', 'You tried to grant access to user [' + targetUser + '] who is forbidden for the table [' + targetTable + ']')
        print('ERROR: Grant of access to user[' + targetUser + '] on the table [' + targetTable + '] by you is unacceptable!')
        return False

    # Catch invalid granting operation => Trying to grant a table without grantable privilege
    if not canGrant(userName, targetTable):
        # => Sending warning to user log and also SO
        logMessageForSO('Invalid Granting Operation', 'User [' + userName + '] tried to grant [' + targetUser + '] access to [' + targetTable + '] but does not have grantable permission')
        logMessageForRegularUsers(userName, 'Invalid Granting Operation', 'You tried to grant access to [' + targetUser + '] but you do not have grantable permission')
        print('You do not have grantable permission for [' + targetTable + ']')


    # Otherwise, insert into assigned table
    cur.execute("INSERT INTO assigned(user_name, table_name, grantable, forbid_attempt, granted_by) VALUES (?, ?, ?, ?, ?)", (targetUser, targetTable, grantable, 0, userName))
    conn.commit()
    return True

# Add user into forbidden table
def addUserToForbiddenTable(targetUser, targetTable):
    print('User [' + targetUser + '] added on forbid list')
    cur.execute("INSERT INTO forbidden(user_name, table_name) VALUES (?, ?)", (targetUser, targetTable))
    conn.commit()

# Recursively remove revoked privileges
def revokedPrivileges(forbidedUserName, forbidedTableName):
    print('Removoking access granted by user [' + forbidedUserName + '] on table [' + forbidedTableName + ']')

    # First, check if there is user who granted access by forbided user on the forbided table
    cur.execute("SELECT * FROM assigned WHERE granted_by=? AND table_name=?", [forbidedUserName, forbidedTableName])
    queryResult = cur.fetchall()

    # Loop through it and start to remove access
    for row in queryResult:
        # If this user (row["user_name"]) has granted access to the forbided table by someone else, then do not need to call recursively
        # If this user (row["user_name"]) only has been granted by forbided user on the forbided table, then call function recursively
        cur.execute("SELECT COUNT(*) FROM assigned WHERE user_name=? AND table_name=?", [row["user_name"], forbidedTableName])
        queryResult = cur.fetchone()
        shouldCallRecursively = False
        if queryResult[0] == 1:
            shouldCallRecursively = True

        # First, remove access to the table if a user is granted access by forbided user on forbided table
        cur.execute("DELETE FROM assigned WHERE user_name=? AND table_name=? AND granted_by=?", [row["user_name"], forbidedTableName, forbidedUserName])
        conn.commit()

        if shouldCallRecursively == True:
            revokedPrivileges(row["user_name"], forbidedTableName)

# Forbid access of user to target table
def forbidAccess(userName, isUserSO, targetUser, targetTable):
    isUserForbid = False

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
                logMessageForSO('Forbidding User Error', 'User [' + targetUser + '] already has access to the table [' + targetTable + ']. Operation stopped.')
                cur.execute("UPDATE assigned SET forbid_attempt = 1 WHERE user_name=? AND table_name=?", (targetUser, targetTable))
                conn.commit()
            # If this is second forbid attempt, then just remove it from assigned table
            # And add to forbidden table
            elif queryResult["forbid_attempt"] == 1:
                logMessageForSO('Overwriting Warning', 'User [' + targetUser + '] will be removed from assigned table for [' + targetTable + '] table. It will revoke all granted access from the user.')
                cur.execute("DELETE FROM assigned WHERE user_name=? AND table_name=?", (targetUser, targetTable))
                conn.commit()
                addUserToForbiddenTable(targetUser, targetTable)
                isUserForbid = True
        else:
            # Add target user into forbidden table
            addUserToForbiddenTable(targetUser, targetTable)
            isUserForbid = True

        # Traverse grant graph recursively to remove revoked privileges by forbid operation
        if isUserForbid == True:
            revokedPrivileges(targetUser, targetTable)
            return True

    else:
        print('You do not have privilege to access system table')
        # Regular user tried to write forbidden table => report to SO
        logMessageForSO('ERROR', 'Regular user [' + userName + '] tried to forbid access of [' + targetUser + '] on table [' + targetTable + ']')
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

# Recursively checks if user has grantable and subsequent parents have grantable
def canGrant(username, tableName):
    # Base case (all paths should have admin as their root)
    if username == 'admin':
        return True

    # Check if they have grantable
    cur.execute("SELECT grantable, granted_by FROM assigned WHERE user_name=? and table_name=?", [username,tableName])
    queryResult = cur.fetchall()
    for row in queryResult:
        # If they have grantable, recursively check if parent has grantable
        if row[0] == 1:
            return canGrant(row[1], tableName)

    return False

# Recursively checks if user has grantable and subsequent parents have grantable
def canAccess(username, tableName):
    # Check who gave them access to table
    cur.execute("SELECT granted_by FROM assigned WHERE user_name=? and table_name=?", [username,tableName])
    queryResult = cur.fetchall()

    # Check if parent is allowed to give them access
    for parent in queryResult:
        if canGrant(parent[0], tableName):
            return True

    # If all parents did not have grantable or user have entry in assigned table
    return False
