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

        self.loginUserNameLabel = Label(master, text="Login user name:").grid(row=0, column=0)
        self.loginUserNameEntry = Entry(master)
        self.loginUserNameEntry.grid(row=0, column=1)

        self.loginButton = Button(master, text="Login", command=self.loginUser)
        self.loginButton.grid(row=0, column=2)

        self.logoutButton = Button(master, text="Logout", command=self.logoutUser)
        self.logoutButton.grid(row=0, column=3)

        self.operationLabel = Label(master, text="Operation:").grid(row=1, column=0)
        self.operationEntry = Entry(master)
        self.operationEntry.grid(row=1, column=1)

        self.inputArg1Label = Label(master, text="Input Arg 1:").grid(row=1, column=2)
        self.inputArg1Entry = Entry(master)
        self.inputArg1Entry.grid(row=1, column=3)

        self.inputArg2Label = Label(master, text="Input Arg 2:").grid(row=1, column=4)
        self.inputArg2Entry = Entry(master)
        self.inputArg2Entry.grid(row=1, column=5)

        self.inputArg3Label = Label(master, text="Input Arg 3:").grid(row=1, column=6)
        self.inputArg3Entry = Entry(master)
        self.inputArg3Entry.grid(row=1, column=7)

        self.runQuery = Button(master, text='Run query', command=self.runQuery).grid(row=2, column=0)
        self.quitButton = Button(master, text='Quit', command=master.quit).grid(row=2, column=1)
        
    def runQuery(self):
        print(self.operationEntry.get())
        print(self.inputArg1Entry.get())
        print(self.inputArg2Entry.get())
        print(self.inputArg3Entry.get())

    def loginUser(self):
        # Check if user name exists in the database
        userInput = self.loginUserNameEntry.get()
        isUserExist, isUserSO = tryToLoginUser(userInput)

        if isUserExist:
            # If user exists in user table, passed
            userLoggedIn = True
            userName = userInput
        else:
            # otherwise, keep asking user name
            print('Please enter correct user name!')

    print('Please enter correct user name!')
    def logoutUser(self):
        userLoggedIn = False
        userName = ''
        print("user logged out!")

    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = projectGUI(root)
root.mainloop()

closeDB()
