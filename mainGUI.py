from Tkinter import *
from db import *

class projectGUI:

    def __init__(self, master):
        self.master = master
        master.title("CS 505 Project 1 GUI")

        self.operationLabel = Label(master, text="Operation:").grid(row=0, column=0)
        self.operationEntry = Entry(master)
        self.operationEntry.grid(row=0, column=1)

        self.inputArg1Label = Label(master, text="Input Arg 1:").grid(row=0, column=2)
        self.inputArg1Entry = Entry(master)
        self.inputArg1Entry.grid(row=0, column=3)

        self.inputArg2Label = Label(master, text="Input Arg 2:").grid(row=0, column=4)
        self.inputArg2Entry = Entry(master)
        self.inputArg2Entry.grid(row=0, column=5)

        self.inputArg3Label = Label(master, text="Input Arg 3:").grid(row=0, column=6)
        self.inputArg3Entry = Entry(master)
        self.inputArg3Entry.grid(row=0, column=7)

        self.runQuery = Button(master, text='Run query', command=self.runQuery).grid(row=1, column=0)

    def runQuery(self):
        print(self.operationEntry.get())
        print(self.inputArg1Entry.get())
        print(self.inputArg2Entry.get())
        print(self.inputArg3Entry.get())


    def greet(self):
        print("Greetings!")

root = Tk()
my_gui = projectGUI(root)
root.mainloop()
