from db import *


# Start sqlite3 database
startDB()

# Create pre-defined user table
createUserTable()

# Create empty system tables (assigned, forbidden, dblog)
createSystemTables()

# Current user related variables
userLoggedIn = False
userName = ''
isUserSO = False

while True:
    if userLoggedIn:
        userInput = raw_input(userName + '> ')
        if userInput == 'q' or userInput == 'quit':
            break
        elif userInput == 'logout':
            userLoggedIn = False
            userName = ''
        else:
            if checkValidQuery(userInput):
                performQuery(userName, isUserSO, userInput)
    else:
        userInput = raw_input('Enter user name: ')
        if userInput == 'q' or userInput == 'quit':
            break

        # Check if user name exists in the database
        isUserExist, isUserSO = tryToLoginUser(userInput)

        if isUserExist:
            # If user exists in user table, passed
            userLoggedIn = True
            userName = userInput
        else:
            # otherwise, keep asking user name
            print('Please enter correct user name!')

closeDB()
