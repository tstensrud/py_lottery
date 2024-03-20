#
# CLASS USERS
#
class Users:
    def __init__(self, name, username, userId, email, password):
        self.name = name
        self.username = username
        self.userId = userId
        self.email = email
        self.password = password

    #getters
    def getName(self):
        return self.name
    def getUsername(self):
        return self.userName
    def getUserId(self):
        return self.userId
    def getEmail(self):
        return self.email
    #setters
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
    def ___init__(self, ticketId, rows, belongsToUser):
        self.ticketId = ticketId
        self.rows = {}
        self.belongsToUser = belongsToUser

    def createRows(self,numberOfRows):
        for i in range (numberOfRows):
            self.rows[i] = 10
    
    def setRows(self):
        pass