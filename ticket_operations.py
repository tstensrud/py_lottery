import os
import random
from classes import Ticket, Operations

class Ticket_Operations(Operations):
    def __init__(self):
        try:
            self.active_tickets = len(self.read_database("t")) # total active Ticket-objects
            self.archived_tickets = len(self.read_database("a")) # total archived Ticket-objects
        except EOFError:
            self.add_dummy_tickets()
            self.active_tickets = len(self.read_database("t"))
            self.archived_tickets = len(self.read_database("a"))

        self.numbers_per_row = 0  # max numbers per row
        self.cost_per_row = 0 # cost per row
        self.max_playable_numbers = 0 # total amount of numbers or "balls" that can be in play
        self.total_income = 0
        self.current_price_pool = 0
        self.jackpot = 0
        self.load_game_info(False)

    # add some dummy tickets if the ticket-file is empty
    def add_dummy_tickets(self):
        file_size = os.path.getsize("./data/tickets.pkl")
        if file_size == 0:
            tickets = []
            tickets.append(Ticket(-1,1,1,1))
            tickets.append(Ticket(-2,1,1,1))
            self.write_to_database(tickets, "t")
        
        file_size_a = os.path.getsize("./data/ticketarchive.pkl")
        if file_size_a == 0:
            tickets = []
            tickets.append(Ticket(-3,1,1,1))
            tickets.append(Ticket(-4,1,1,1))
            self.write_to_database(tickets, "a")
    
    # method runs when program starting to sett contructor-variables to latest settings
    # method also is called when one of the variables need updating du to changes while program is running
    # update is set to False upon load of program, True when its to update the variables
    def load_game_info(self, update):
        if update == False:
            json_file_size = os.path.getsize("./data/game_info.json")
            # first time program is run these values are initialized
            if json_file_size == 0:
                game_info = {
                    "numbers_per_row" : 8,
                    "cost_per_row" : 10,
                    "max_playable_numbers" : 40,
                    "total_income" : 0,
                    "current_price_pool" : 0,
                    "jackpot" : 0
                }
                self.write_to_json(game_info)
        
            game_info = self.read_gameinfo_json()
            self.numbers_per_row = game_info["numbers_per_row"]
            self.cost_per_row = game_info["cost_per_row"]
            self.max_playable_numbers = game_info["max_playable_numbers"]
            self.total_income = game_info["total_income"]
            self.current_price_pool =  game_info["current_price_pool"]
            self.jackpot = game_info["jackpot"]
        
        elif update == True:
            game_info = self.read_gameinfo_json()
            game_info["numbers_per_row"] = self.numbers_per_row
            game_info["cost_per_row"] = self.cost_per_row
            game_info["max_playable_numbers"] = self.max_playable_numbers
            game_info["total_income"] = self.total_income
            game_info["current_price_pool"] = self.current_price_pool
            game_info["jackpot"] = self.jackpot
            self.write_to_json(game_info)

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
        tickets = self.read_database("t")
        rows_in_new_ticket = [None]*rows
        ticket_id = self.archived_tickets + len(tickets) + 1
        ticket_cost = self.ticket_cost(rows)
        for i in range(rows):
            rows_in_new_ticket[i] = self.new_row()
        tickets.append(Ticket(ticket_id, rows_in_new_ticket, user_id, ticket_cost))
        self.active_tickets = len(tickets)
        self.write_to_database(tickets, "t")
        self.load_game_info(True)
        return ticket_id

    
    # calculate price of ticket and add it to total income
    def ticket_cost(self, rows):
        ticket_cost = rows * self.cost_per_row
        self.total_income += ticket_cost
        self.current_price_pool += ticket_cost
        return ticket_cost

    # get total income
    def get_income(self):
        return self.total_income
    
    # get current price pool
    def get_current_price_pool(self):
        return self.current_price_pool
    
    # get jackpot status
    def get_jackpot(self):
        return self.jackpot
    
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
        tickets = self.read_database("t")
        for i in range(len(tickets)):
            if tickets[i].get_ticket_id() == ticket_id:
                return tickets[i]
        return None

    # return ticket object from archivedTickets
    def get_archived_ticket(self, ticket_id):
        archive = self.read_database("a")
        for i in range(len(archive)):
            if archive[i].get_ticket_id() == ticket_id:
                return archive[i]
        return None
    
    # reset game. adds all active tickets to archived, and clears active tickets list
    def reset_game(self):
        archive = self.read_database("a")
        active_tickets = self.read_database("t")
        # add active tickets to archive
        for i in range(len(active_tickets)):
            archive.append(active_tickets[i])
        
        # empty active tickets file with an empty list
        active_tickets = []
        self.write_to_database(active_tickets, "t")
        self.current_price_pool = 0
        self.archived_tickets += len(archive)
        self.active_tickets = len(active_tickets)
        self.write_to_database(archive, "a")

    # find winning tickets. return ticket-object that has a row who matches the winning_row
    def find_winning_tickets(self, winning_row):
        winners = []
        for i in range(len(self.active_tickets)):
            ticket = self.active_tickets[i]
            ticket_rows = ticket.get_rows()
            for j in range(len(ticket_rows)):
                for k in range(len(ticket_rows[j])):
                    if ticket_rows[j][k] == winning_row:
                        winners.append(ticket)
        if len(winners) == 0:
            self.jackpot += self.current_price_pool
        else:
            self.jackpot = 0
        return winners