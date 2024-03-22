import sys
from tkinter import messagebox
from ticket_operations import Ticket_Operations
from user_operations import User_Operations
from tkinter import *
import tkinter as tk

ticket_operations = Ticket_Operations()
user_operations = User_Operations()
currentWinnerNumbers = [None]*ticket_operations.numbersPerRow
totalFrames = 7
framesList = []

def main():
    
    user_operations.addNewUser("NAVN", "BRUKERNAVN", "E@B.C", "PASSOWRD")

    def exit():
        sys.exit()
    
       
    def addNewTicket():
        try:
            userId = int(newTicketUserIdTextField.get())
        except ValueError:
            messagebox.showinfo("Error", f"User ID can only contain digits")
            return
        if user_operations.doesUserExist(userId) == False:
            messagebox.showinfo("Error", f"User id \"{userId}\" not found")
            return
        rows = rowChoice.get()
        ticket_operations.addNewTicket(rows, userId)


    # switching frames from menu options
    # hides all frames that is not menuItem.
    def frameSelectionFromMenu(menuItem):
        for i in range(len(framesList)):
            if i != menuItem:
                framesList[i].forget()
            else:
                framesList[i].pack(fill="both", expand=1) 

    def drawNewSetOfWinningNumbers():
        currentWinnerNumbers = ticket_operations.generateWinningNumbers()

    #main window
    mainWindow = tk.Tk()
    mainWindow.geometry("1024x768")
    mainWindow.title("Lottery")
    
    '''
    FRAMES
    0 = default
    1 = game options
    2 = new ticket
    3 = ticket stats
    4 = add user
    5 = user stats
    6 = find user
    '''
    for i in range(totalFrames):
        frame = tk.Frame(mainWindow)
        framesList.append(frame)
    
    welcomeLabel = tk.Label(framesList[0], text="Use menu to start")
    welcomeLabel.pack()
    framesList[0].pack(fill="both", expand=1)

    gameStatsLabel = tk.Label(framesList[1], text="GAME OPTIONS")
    gameStatsLabel.pack()

    ## NEW TICKET FRAME
    newTicketLabel = tk.Label(framesList[2], text="NEW TICKET")
    newTicketLabel.pack()
    newTicketRowsLabel = tk.Label(framesList[2], text="How many rows in ticket: ")
    newTicketUserIdLabel = tk.Label(framesList[2], text="User ID")
    newTicketRowsLabel.place(x=10, y=50)
    newTicketUserIdLabel.place(x=10, y=100)
    newTicketUserIdTextField = tk.Entry(framesList[2], width=10)
    newTicketUserIdTextField.place(x=170, y=100)
    rowOptions = [1,2,3,4,5,6,7,8,9,10]
    rowChoice = tk.IntVar(framesList[2])
    rowChoice.set(10)
    rowOptionsMenu = tk.OptionMenu(framesList[2], rowChoice, *rowOptions)
    rowOptionsMenu.place(x=170, y=50)
    newTicketButton = tk.Button(framesList[2], text="New ticket", width=10, height=1, command=addNewTicket)
    newTicketButton.place(x=10, y=150)

    ticketStatsLabel = tk.Label(framesList[3], text="TICKET STATS")
    ticketStatsLabel.pack()

    addUserLabel = tk.Label(framesList[4], text="ADD USER")
    addUserLabel.pack()

    userStatsLabel = tk.Label(framesList[5], text="USER STATS")
    userStatsLabel.pack()

    findUserLabel = tk.Label(framesList[6], text="FIND USER")
    findUserLabel.pack()

    #
    # TOP MENU
    #
    menuBar = Menu(mainWindow)
    
    #file menu (1)
    menuBarFileMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="File", menu=menuBarFileMenu)
    menuBarFileMenu.add_command(label="Game options", command=lambda: frameSelectionFromMenu(1))
    menuBarFileMenu.add_separator()
    menuBarFileMenu.add_command(label="Exit", command=exit)
    
    
    #tickets menu (2.3)
    menuBarTicketsMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Ticket", menu=menuBarTicketsMenu)
    menuBarTicketsMenu.add_command(label="New ticket", command=lambda: frameSelectionFromMenu(2))
    menuBarTicketsMenu.add_command(label="Ticket stats", command=lambda: frameSelectionFromMenu(3))
    

    #users menu (4, 5, 6)
    menuBarUsersMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Users", menu=menuBarUsersMenu)
    menuBarUsersMenu.add_command(label="Add new user", command=lambda: frameSelectionFromMenu(4))
    menuBarUsersMenu.add_command(label="User statistics", command=lambda: frameSelectionFromMenu(5))
    menuBarUsersMenu.add_command(label="Find user", command=lambda: frameSelectionFromMenu(6))
    

    mainWindow.config(menu=menuBar)
    mainWindow.config()
    mainWindow.mainloop()

if __name__ == "__main__":
    main()























