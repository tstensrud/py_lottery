import random
#
# CLASS USERS
#
class User:
    def __init__(self, name, user_id, email, phone_number, password):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.phone_number = phone_number
        self.password = password

    #GETTERS
    def get_name(self):
        return self.name
    def get_user_id(self):
        return self.user_id
    def get_email(self):
        return self.email
    #SETTERS
    def set_username(self, username):
        self.username = username
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password
    

#
# CLASS TICKET
#
class Ticket:
    def __init__(self, ticket_id, rows, user_id):
        self.ticketId = ticket_id
        self.rows = [rows]
        self.userId = user_id
    
    # GETTERS
    def get_ticket_id(self):
        return self.ticketId
    def get_user_id(self):
        return self.userId
    def get_rows(self):
        return self.rows