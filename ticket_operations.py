'''
This module is for all functions that do operations on the Ticket-objects.
'''
import random
from classes import Ticket
activeTickets = [] #list of archived Ticket-objects
archivedTickets = [] #list of active Ticket-objects
numbersPerRow = 8 #max numbers per row
maxPlayableNumbers = 40 #total amount of numbers or "balls" that can be in play

# add new ticket with n-rows pointed to a specific user
def addNewTicket(rows, userId):
    rowsInNewTicket = [None]*rows
    for i in range(rows):
        rowsInNewTicket[i] = newRow()
    activeTickets.append(Ticket(len(activeTickets)+1, rowsInNewTicket, userId))

# used to find duplicate number when generating a row with random numbers
def findDouplicate(row, number):
    for i in range(len(row)):
        if (row[i] == number):
            return True
    return False

# generate a row of random numbers and return it sorted in ascending order. Check for duplicate number.
def newRow():
    row = [None]*numbersPerRow
    for i in range(len(row)):
        row[i] = 0
    randomNumber = random.randint(1,40)
    for i in range(len(row)):
        while findDouplicate(row, randomNumber):
            randomNumber = random.randint(1,maxPlayableNumbers)
        row[i] = randomNumber
    return sorted(row)

# return ticket object from activeTickets
def getActiveTicket(ticketId):
    for i in range(len(activeTickets)):
        if activeTickets[i].getTicketId() == ticketId:
            return activeTickets[i]

# return ticket object from archivedTickets
def getArchivedTicket(ticketId):
    for i in range(len(archivedTickets)):
        if archivedTickets[i].getTicketId() == ticketId:
            return archivedTickets[i]
        
# reset game. adds all active tickets to archived, and clears active tickets list
