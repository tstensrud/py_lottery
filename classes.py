import random
#
# CLASS USERS
#
class User:
    def __init__(self, name, userName, userId, email, password):
        self.name = str(name)
        self.userName = str(userName)
        self.userId = int(userId)
        self.email = str(email)
        self.password = str(password)

    #GETTERS
    def getName(self):
        return self.name
    def getUserName(self):
        return self.userName
    def getUserId(self):
        return self.userId
    def getEmail(self):
        return self.email
    #SETTERS
    def setEmail(self, email):
        self.email = email
    def setUsername(self, username):
        self.username = username
    def setEmail(self, email):
        self.email = email
    def setPassword(self, password):
        self.password = password
    

#
# CLASS TICKET
#
class Ticket:
    def __init__(self, ticketId, rows, userId):
        self.ticketId = int(ticketId)
        self.rows = []
        self.userId = int(userId)
    
    # GETTERS
    def getTicketId(self):
        return self.ticketId
    def getUserId(self):
        return self.userId
    def getRows(self):
        return self.rows