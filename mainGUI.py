from Tkinter import *
from db import *

# Start sqlite3 database
startDB()

# Create pre-defined user table
createUserTable()

# Create empty system tables (assigned, forbidden, dblog)
createSystemTables()

# Create regular tables (emp, salary)
createRegularTables()

establishSampleCase()

class projectGUI:

    def __init__(self, master):
        # Current user related variables
        self.userLoggedIn = False
        self.userName = ''
        self.isUserSO = False

        self.master = master
        master.title("CS 505 Project 1 GUI")

        userList = getUsers()#["admin","marek","dexter","boxter","tester","worker"]

        self.loginUserLabel = Label(master, text="User Name:").grid(row=0, column=0)
        self.loginUserOptionListVar = StringVar()
        self.loginUserOptionListVar.set(userList[0])
        self.currentLoggedInUser = userList[0]
        self.loginUserOptionMenu = OptionMenu(master, self.loginUserOptionListVar, *userList, command=self.updateLoginUser)
        self.loginUserOptionMenu.grid(row=0, column=1)

        self.loginButton = Button(master, text="Login", command=self.loginUser)
        self.loginButton.grid(row=0, column=2)

        self.logoutButton = Button(master, text="Logout", state=DISABLED, command=self.logoutUser)
        self.logoutButton.grid(row=0, column=3)

        self.operationLabel = Label(master, text="Operation:").grid(row=1, column=0)
        operationOptionList = ["ACCESS","REVOKE","FORBID","GRANT","GRANT WITH GRANT OPTION","PRINT"]
        self.operationOptionListVar = StringVar()
        self.operationOptionListVar.set(operationOptionList[0])
        self.currentOperation = operationOptionList[0].lower()
        self.operationOptionMenu = OptionMenu(master, self.operationOptionListVar, *operationOptionList, command=self.updateOperation)
        self.operationOptionMenu['state'] = 'disabled'
        self.operationOptionMenu.grid(row=1, column=1)

        self.targetUserLabel = Label(master, text="Target User:").grid(row=1, column=2)
        self.targetUserOptionListVar = StringVar()
        self.targetUserOptionListVar.set(userList[0])
        self.currentTargetUser = userList[0]
        self.targetUserOptionMenu = OptionMenu(master, self.targetUserOptionListVar, *userList, command=self.updateTargetUser)
        self.targetUserOptionMenu['state'] = 'disabled'
        self.targetUserOptionMenu.grid(row=1, column=3)

        self.targetTableLabel = Label(master, text="Target Table:").grid(row=1, column=4)
        targetTableOptionList = ["salary","reglog","assigned","forbidden","dblog"]
        self.targetTableOptionListVar = StringVar()
        self.targetTableOptionListVar.set(targetTableOptionList[0])
        self.currentTargetTable = targetTableOptionList[0]
        self.targetTableOptionMenu = OptionMenu(master, self.targetTableOptionListVar, *targetTableOptionList, command=self.updateTargetTable)
        self.targetTableOptionMenu['state'] = 'disabled'
        self.targetTableOptionMenu.grid(row=1, column=5)

        self.runQueryButton = Button(master, text='Run query', state=DISABLED, command=self.runQuery)
        self.runQueryButton.grid(row=1, column=6)
        self.quitButton = Button(master, text='Quit', command=master.quit).grid(row=1, column=7)

        self.textBox = Text(master, borderwidth=1, width=100, height=25)
        self.textBox.grid(row=2, columnspan=8)

    def printToTextBox(self, message):
        try:
            self.textBox['state']='normal'
            self.textBox.insert(END, str(message) + "\n")
            self.textBox.see(END)
            self.textBox['state']='disabled'
            self.textBox.update()
        except TclError, e:
          print(e)

    def updateLoginUser(self, value):
        self.currentLoggedInUser = value.lower()

    def updateOperation(self, value):
        self.currentOperation = value.lower()
        # If selected operation is 'print' or 'access', disable target user combo box
        if self.currentOperation == 'print' or self.currentOperation == 'access':
            self.targetUserOptionMenu['state'] = 'disabled'
        else:
            self.targetUserOptionMenu['state'] = 'normal'

    def updateTargetUser(self, value):
        self.currentTargetUser = value.lower()

    def updateTargetTable(self, value):
        self.currentTargetTable = value.lower()

    def runQuery(self):
        queryOperation = self.currentOperation
        queryTargetUser = self.currentTargetUser
        queryTargetTable = self.currentTargetTable
        query = ''

        if self.currentOperation == 'print' or self.currentOperation == 'access':
            query = queryOperation + " " + queryTargetTable
        elif self.currentOperation == 'grant with grant option':
            query = "grant " + queryTargetUser + " " + queryTargetTable + " grantable"
        else:
            query = queryOperation + " " + queryTargetUser + " " + queryTargetTable;

        checkQueryResult, checkQueryReturnStr = checkValidQuery(query)
        self.printToTextBox(checkQueryReturnStr)

        if checkQueryResult:
            queryRet, queryRetStr = performQuery(self.userName, self.isUserSO, query)
            self.printToTextBox(queryRetStr + '\n')

    def loginUser(self):
        # Check if user name exists in the database
        userInput = self.currentLoggedInUser
        isUserExist, self.isUserSO, returnMessage = tryToLoginUser(userInput)
        self.printToTextBox(returnMessage)

        if isUserExist:
            # If user exists in user table, passed
            self.userLoggedIn = True
            self.userName = userInput
            self.loginButton['state'] = 'disabled'
            self.logoutButton['state'] = 'normal'
            self.runQueryButton['state'] = 'normal'
            self.operationOptionMenu['state'] = 'normal'
            if self.currentOperation == 'print' or self.currentOperation == 'access':
                self.targetUserOptionMenu['state'] = 'disabled'
            self.targetTableOptionMenu['state'] = 'normal'
        else:
            # otherwise, keep asking user name
            print('Please enter correct user name!')

    def logoutUser(self):
        self.userLoggedIn = False
        self.userName = ''
        self.loginButton['state']='normal'
        self.logoutButton['state']='disabled'
        self.runQueryButton['state']='disabled'
        self.printToTextBox('Logged out!')
        self.operationOptionMenu['state'] = 'disabled'
        self.targetUserOptionMenu['state'] = 'disabled'
        self.targetTableOptionMenu['state'] = 'disabled'

root = Tk()
my_gui = projectGUI(root)
root.mainloop()

closeDB()
