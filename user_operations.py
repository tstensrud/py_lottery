from classes import User

class User_Operations:
    def __init__(self):
        self.users = []

    def addNewUser(self, name, userName, email, password):
        getUserCount = len(self.users)
        newUserId = getUserCount + 1
        self.users.append(User(name, userName, newUserId, email, password))

    #see if userID exists
    def doesUserExist(self, userId):
        for i in range (len(self.users)):
            if self.users[i].getUserId() == userId:
                return True
        return False