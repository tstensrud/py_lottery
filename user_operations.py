from classes import User

class User_Operations:
    def __init__(self):
        self.users = []

    def add_new_user(self, name, email, phone_number, password):
        get_user_count = len(self.users)
        new_user_id = get_user_count + 1
        self.users.append(User(name, new_user_id, email, phone_number, password))

    #see if userID exists
    def does_user_exist(self, user_id):
        for i in range (len(self.users)):
            if self.users[i].get_user_id() == user_id:
                return True
        return False
