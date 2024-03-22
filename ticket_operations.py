import random
from classes import Ticket

class Ticket_Operations:
    def __init__(self):
        self.activeTickets = [] #list of archived Ticket-objects
        self.archivedTickets = [] #list of active Ticket-objects
        self.numbersPerRow = 8 #max numbers per row
        self.maxPlayableNumbers = 40 #total amount of numbers or "balls" that can be in play

    # draw a row of winning numbers. Once a number is drawn it's removed from the pool of available numbers
    def generateWinningNumbers(self):
        availableNumbers = [None]*self.maxPlayableNumbers #define array of playable numbers
        for i in range(self.maxPlayableNumbers):
            availableNumbers[i] = i+1 #add numbers from 1 to n-playable numbers, defined by maxPlayableNumbers (40 default)
        winningNumbers = [None]*self.numbersPerRow #set up local list of winning numbers, max defined by numbersPerRow
        for i in range(len(winningNumbers)):
            num = random.choice(availableNumbers) #select random number from available number and add it to winningNumbers
            winningNumbers[i] = num
            availableNumbers.remove(num) #remove num from pool of available numbers, simulating balls in a physical lottery
        return sorted(winningNumbers)

    # set numbers per row
    def setNumbersPerRow(self, newNumber):
        if newNumber > 0:
            self.numbersPerRow = newNumber
        else:
            raise ValueError("Number must be > 0")

    #set max playable numbers
    def setMaxPlayableNumbers(self,newNumber):
        if newNumber > 0:
            self.maxPlayableNumbers = newNumber
        else:
            raise ValueError("Number must be > 0")

    # add new ticket with n-rows pointed to a specific user
    def addNewTicket(self,rows, userId):
        rowsInNewTicket = [None]*rows
        for i in range(rows):
            rowsInNewTicket[i] = self.newRow()
        self.activeTickets.append(Ticket(len(self.activeTickets)+1, rowsInNewTicket, userId))

    # used to find duplicate number when generating a row with random numbers
    def findDouplicate(self, row, number):
        for i in range(len(row)):
            if (row[i] == number):
                return True
        return False

    # generate a row of random numbers and return it sorted in ascending order. Check for duplicate number.
    def newRow(self):
        row = [None]*self.numbersPerRow
        for i in range(len(row)):
            row[i] = 0
        randomNumber = random.randint(1,40)
        for i in range(len(row)):
            while self.findDouplicate(row, randomNumber):
                randomNumber = random.randint(1,self.maxPlayableNumbers)
            row[i] = randomNumber
        return sorted(row)

    # return ticket object from activeTickets
    def getActiveTicket(self, ticketId):
        for i in range(len(self.activeTickets)):
            if self.activeTickets[i].getTicketId() == ticketId:
                return self.activeTickets[i]

    # return ticket object from archivedTickets
    def getArchivedTicket(self, ticketId):
        for i in range(len(self.archivedTickets)):
            if self.archivedTickets[i].getTicketId() == ticketId:
                return self.archivedTickets[i]
    
    # reset game. adds all active tickets to archived, and clears active tickets list
    def resetGame(self):
        for i in range(len(self, self.activeTickets)):
            self.archivedTickets.append(self.activeTickets[i])
        self.activeTickets.clear()

