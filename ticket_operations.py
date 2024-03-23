import random
from classes import Ticket

class Ticket_Operations:
    def __init__(self):
        self.activeTickets = [] #list of archived Ticket-objects
        self.archivedTickets = [] #list of active Ticket-objects
        self.numbers_per_row = 8 #max numbers per row
        self.max_playable_numbers = 40 #total amount of numbers or "balls" that can be in play

    # draw a row of winning numbers. Once a number is drawn it's removed from the pool of available numbers
    def generate_winning_numbers(self):
        available_numbers = [None]*self.max_playable_numbers #define array of playable numbers
        for i in range(self.max_playable_numbers):
            available_numbers[i] = i+1 #add numbers from 1 to n-playable numbers, defined by maxPlayableNumbers (40 default)
        winning_numbers = [None]*self.numbers_per_row #set up local list of winning numbers, max defined by numbersPerRow
        for i in range(len(winning_numbers)):
            num = random.choice(available_numbers) #select random number from available number and add it to winningNumbers
            winning_numbers[i] = num
            available_numbers.remove(num) #remove num from pool of available numbers, simulating balls in a physical lottery
        return sorted(winning_numbers)

    # set numbers per row
    def set_numbers_per_row(self, new_number):
        if new_number > 0:
            self.numbers_per_row = new_number
        else:
            raise ValueError("Number must be > 0")

    #set max playable numbers
    def set_max_playable_numbers(self, new_number):
        if new_number > 0:
            self.max_playable_numbers = new_number
        else:
            raise ValueError("Number must be > 0")

    # add new ticket with n-rows pointed to a specific user
    def add_new_ticket(self, rows, user_id):
        rows_in_new_ticket = [None]*rows
        for i in range(rows):
            rows_in_new_ticket[i] = self.new_row()
        self.activeTickets.append(Ticket(len(self.activeTickets) + 1, rows_in_new_ticket, user_id))

    # used to find duplicate number when generating a row with random numbers
    def find_douplicate(self, row, number):
        for i in range(len(row)):
            if row[i] == number:
                return True
        return False

    # generate a row of random numbers and return it sorted in ascending order. Check for duplicate number.
    def new_row(self):
        row = [None]*self.numbers_per_row
        for i in range(len(row)):
            row[i] = 0
        random_number = random.randint(1,40)
        for i in range(len(row)):
            while self.find_douplicate(row, random_number):
                random_number = random.randint(1, self.max_playable_numbers)
            row[i] = random_number
        return sorted(row)

    # return ticket object from activeTickets
    def get_active_ticket(self, ticket_id):
        for i in range(len(self.activeTickets)):
            if self.activeTickets[i].get_ticket_id() == ticket_id:
                return self.activeTickets[i]

    # return ticket object from archivedTickets
    def get_archived_ticket(self, ticket_id):
        for i in range(len(self.archivedTickets)):
            if self.archivedTickets[i].get_ticket_id() == ticket_id:
                return self.archivedTickets[i]
    
    # reset game. adds all active tickets to archived, and clears active tickets list
    def reset_game(self):
        for i in range(len(self.activeTickets)):
            self.archivedTickets.append(self.activeTickets[i])
        self.activeTickets.clear()

