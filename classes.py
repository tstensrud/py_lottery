import datetime
#
# CLASS USERS
#
class User:
    def __init__(self, name, user_id, email, phone_number, password):
        self.name = name
        self.user_id = int(user_id)
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.active_tickets = []
        self.archived_tickets = []
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
    def get_archived_tickets(self):
        return self.archived_tickets
    def get_date(self):
        return self.created_when
    #SETTERS
    def set_username(self, username):
        self.username = username
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password

    def add_active_ticket(self, ticketid):
        self.active_tickets.append(ticketid)
    def move_active_to_archived(self):
        for ticket in self.active_tickets:
            self.archived_tickets.append(ticket)
    def clear_active_tickets(self):
        self.active_tickets.clear()
    

#
# CLASS TICKET
#
class Ticket:
    def __init__(self, ticket_id, rows, user_id, cost):
        self.ticketId = ticket_id
        self.rows = [rows]
        self.userId = user_id
        self.cost = cost
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