import random
from classes import Ticket

class Ticket_Operations:
    def __init__(self):
        self.active_tickets = [] # list of archived Ticket-objects
        self.archived_tickets = [] # list of active Ticket-objects
        self.ticket_id = 1000
        self.numbers_per_row = 8 # max numbers per row
        self.cost_per_row = 10 # cost per row
        self.max_playable_numbers = 40 # total amount of numbers or "balls" that can be in play
        self.total_income = 0

    # draw a row of winning numbers. Once a number is drawn it's removed from the pool of available numbers
    def generate_winning_numbers(self):
        available_numbers = [None]*self.max_playable_numbers
        for i in range(self.max_playable_numbers):
            available_numbers[i] = i+1
        winning_numbers = [None]*self.numbers_per_row
        for i in range(len(winning_numbers)):
            num = int(random.choice(available_numbers))
            winning_numbers[i] = num
            available_numbers.remove(num)
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
        self.ticket_id += 1
        ticket_cost = rows * self.cost_per_row
        self.total_income += ticket_cost
        for i in range(rows):
            rows_in_new_ticket[i] = self.new_row()
        self.active_tickets.append(Ticket(self.ticket_id, rows_in_new_ticket, user_id, ticket_cost))
        return self.ticket_id

    # get total income
    def get_income(self):
        return self.total_income

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
        random_number = random.randint(1,self.max_playable_numbers)
        for i in range(len(row)):
            while self.find_douplicate(row, random_number):
                random_number = random.randint(1, self.max_playable_numbers)
            row[i] = random_number
        return sorted(row)

    # return ticket object from activeTickets
    def get_active_ticket(self, ticket_id):
        for i in range(len(self.active_tickets)):
            if self.active_tickets[i].get_ticket_id() == ticket_id:
                return self.active_tickets[i]
        return None

    # return ticket object from archivedTickets
    def get_archived_ticket(self, ticket_id):
        for i in range(len(self.archived_tickets)):
            if self.archived_tickets[i].get_ticket_id() == ticket_id:
                return self.archived_tickets[i]
        return None
    
    # reset game. adds all active tickets to archived, and clears active tickets list
    def reset_game(self):
        for i in range(len(self.active_tickets)):
            self.archived_tickets.append(self.active_tickets[i])
        self.active_tickets.clear()

    # find winning tickets
    def find_winning_tickets(self, winning_row):
        winners = []
        for i in range(len(self.active_tickets)):
            ticket = self.active_tickets[i]
            ticket_rows = ticket.get_rows()
            for j in range(len(ticket_rows)):
                for k in range(len(ticket_rows[j])):
                    if ticket_rows[j][k] == winning_row:
                        winners.append(ticket)                  
        return winners