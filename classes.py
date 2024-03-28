import datetime
import json
import pickle
import os
#
# CLASS OPERATIONS
# operations that is usable in both ticket_operations and user_operations
#
class Operations:
    def __init__ (self):
        self.add_first_dummy_user()

    # Add a dummy-user if the user-list is empty.
    def add_first_dummy_user(self):
        file_size = os.path.getsize("./data/users.pkl")
        if file_size == 0:
            users = []
            users.append(User("Dummy User", "1", "dummy@email.com", "12345678", "password"))
            users.append(User("Dummier User", "2", "dummier@email.com", "12345678", "password"))
            self.write_to_database(users, "u") 

    # write game_info.json-file
    def write_to_json(self, data):
        file_path = "./data/game_info.json"
        with open(file_path, "w") as game_info:
            json.dump(data, game_info)
    
    # read .json game_info file
    def read_gameinfo_json(self):
        file_path = "./data/game_info.json"
        with open(file_path, "r") as game_info:
            data = json.load(game_info)
        return data
    
    # open and write to archive-file.  'a' for archive. 't' for active tickets. 'u' for users, 'w' for winning numbers
    def write_to_database(self, object_list, database):
        # archive-file
        if database == "a":
            with open("./data/ticketarchive.pkl", "wb") as archive:
                pickle.dump(object_list, archive)
        # tickets-file
        elif database == "t":
            with open("./data/tickets.pkl", "wb") as tickets:
                pickle.dump(object_list, tickets)
        # users-file
        elif database == "u":
            with open("./data/users.pkl", "wb") as users:
                pickle.dump(object_list, users)
        # winners-file
        elif database == "w":
            with open("./data/oldwinners.pkl", "wb") as win:
                pickle.dump(object_list, win)
    
    # open and read file. 'a' for archive. 't' for active tickets. 'u' for users, 'w' for winning numbers
    def read_database(self, database):
        # archive-file
        if database == "a":
            opened_archive = []
            with open("./data/ticketarchive.pkl", "rb") as archive:
                opened_archive = pickle.load(archive)
            return opened_archive
        # tickets-file
        elif database == "t":
            opened_tickets = []
            with open("./data/tickets.pkl", "rb") as tickets:
                opened_tickets = pickle.load(tickets)
            return opened_tickets
        # users-file
        elif database == "u":
            opened_users = []
            with open("./data/users.pkl", "rb") as users:
                opened_users = pickle.load(users)
            return opened_users
        # winning numbers file
        elif database == "w":
            winners = []
            with open("./data/oldwinners.pkl", "rb") as win:
                winners = pickle.load(win)
            return winners
    


    # empty ticket-databases
    def reset_database(self, database):
        if database == "a":
            open("./data/ticketarchive.pkl", "w").close()
        elif database == "t":
            open("./data/tickets.pkl", "w").close()
        elif database == "u":
            open("./data/users.pkl", "w").close()

#
# CLASS USERS
# class for user-objects
#
class User:
    def __init__(self, name, user_id, email, phone_number, password):
        self.name = name
        self.user_id = int(user_id)
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.active_tickets = []
        self.created_when = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #GETTERS
    def get_name(self):
        return self.name
    def get_user_id(self):
        return self.user_id
    def get_email(self):
        return self.email
    def get_active_tickets(self):
        return self.active_tickets
    def get_date(self):
        return self.created_when
    #SETTERS
    def set_username(self, username):
        self.username = username
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password

    def add_ticket(self, ticketid):
        self.active_tickets.append(ticketid)


#
# CLASS TICKET
# class for ticket-objects
#
class Ticket:
    def __init__(self, ticket_id, rows, user_id, cost):
        self.ticketId = ticket_id
        self.rows = [rows]
        self.userId = user_id
        self.cost = cost
        self.active = True
        self.created_when = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # GETTERS
    def get_ticket_id(self):
        return self.ticketId
    def get_user_id(self):
        return self.userId
    def get_rows(self):
        return self.rows
    def get_ticket_cost(self):
        return self.cost
    def get_date(self):
        return self.created_when
    def get_active(self):
        return self.active
    
    def set_active(self):
        self.active == False