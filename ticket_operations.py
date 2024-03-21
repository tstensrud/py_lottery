'''
This module is for all functions that do operations on the Ticket-objects.
'''
import random
from classes import Ticket
activeTickets = []
archivedTickets = []
numbersPerRow = 8
maxNumbers = 40

#add new ticket
def newTicket(rows, userId):
    totalRows = [None]*rows
    
#used to find duplicate number when generating a row with random numbers
def findDouplicate(self, row, number):
    for i in range(len(row)):
        if (row[i] == number):
            return True
    return False

# generate a row of random numbers
def newRow(self):
    row = [None]*self.numbersPerRow
    for i in range(len(row)):
        row[i] = 0
    randomNumber = random.randint(1,40)
    for i in range(len(row)):
        while self.findDouplicate(row, randomNumber):
            randomNumber = random.randint(1,maxNumbers)
        row[i] = randomNumber
    return sorted(row)
