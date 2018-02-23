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

# Current user related variables
userLoggedIn = False
userName = ''
isUserSO = False

class projectGUI:

    def __init__(self, master):
        self.master = master
        master.title("CS 505 Project 1 GUI")

        userList = ["admin","marek","dexter","boxter","tester","worker"]

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
        operationOptionList = ["ACCESS","GRANT","GRANT WITH GRANT OPTION","PRINT"]
        self.operationOptionListVar = StringVar()
        self.operationOptionListVar.set(operationOptionList[0])
        self.currentOperation = operationOptionList[0].lower()
        self.operationOptionMenu = OptionMenu(master, self.operationOptionListVar, *operationOptionList, command=self.updateOperation)
        self.operationOptionMenu.grid(row=1, column=1)

        self.targetUserLabel = Label(master, text="Target User:").grid(row=1, column=2)
        self.targetUserOptionListVar = StringVar()
        self.targetUserOptionListVar.set(userList[0])
        self.currentTargetUser = userList[0]
        self.targetUserOptionMenu = OptionMenu(master, self.targetUserOptionListVar, *userList, command=self.updateTargetUser)
        self.targetUserOptionMenu.grid(row=1, column=3)

        self.targetTableLabel = Label(master, text="Target Table:").grid(row=1, column=4)
        targetTableOptionList = ["salary","reglog","assigned","forbidden","dblog"]
        self.targetTableOptionListVar = StringVar()
        self.targetTableOptionListVar.set(targetTableOptionList[0])
        self.currentTargetTable = targetTableOptionList[0]
        self.targetTableOptionMenu = OptionMenu(master, self.targetTableOptionListVar, *targetTableOptionList, command=self.updateTargetTable)
        self.targetTableOptionMenu.grid(row=1, column=5)

        self.runQueryButton = Button(master, text='Run query', state=DISABLED, command=self.runQuery)
        self.runQueryButton.grid(row=2, column=0)
        self.quitButton = Button(master, text='Quit', command=master.quit).grid(row=2, column=1)

        self.textBox = Text(master, borderwidth=2, height=20)
        self.textBox.grid(row=3, columnspan=6)

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

    def updateTargetUser(self, value):
        self.currentTargetUser = value.lower()

    def updateTargetTable(self, value):
        self.currentTargetTable = value.lower()

    def runQuery(self):

        #if checkValidQuery(userInput):
        #    performQuery(userName, isUserSO, userInput)

        print(self.currentLoggedInUser)
        print(self.currentOperation)
        print(self.currentTargetUser)
        print(self.currentTargetTable)


    def loginUser(self):
        # Check if user name exists in the database
        userInput = self.currentLoggedInUser
        isUserExist, isUserSO, returnMessage = tryToLoginUser(userInput)
        self.printToTextBox(returnMessage)

        if isUserExist:
            # If user exists in user table, passed
            userLoggedIn = True
            userName = userInput
            self.loginButton['state']='disabled'
            self.logoutButton['state']='normal'
            self.runQueryButton['state']='normal'
        else:
            # otherwise, keep asking user name
            print('Please enter correct user name!')

    def logoutUser(self):
        userLoggedIn = False
        userName = ''
        self.loginButton['state']='normal'
        self.logoutButton['state']='disabled'
        self.runQueryButton['state']='disabled'
        self.printToTextBox('Logged out!')

root = Tk()
my_gui = projectGUI(root)
root.mainloop()

closeDB()
