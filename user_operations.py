from classes import User, Operations
import os

class User_Operations(Operations):
    def __init__(self):
        try:
            self.total_users = len(self.read_database("u"))
        except TypeError:
            self.add_first_dummy_user()
            self.total_users = len(self.read_database("u"))
    
    # Add a dummy-user if the user-list is empty.
    def add_first_dummy_user(self):
        file_size = os.path.getsize("./data/users.pkl")
        if file_size == 0:
            users = []
            users.append(User("Dummy User", -1, "dummy@email.com", "12345678", "password"))
            users.append(User("Dummier User", -2, "dummier@email.com", "12345678", "password"))
            self.write_to_database(users, "u") 

    def add_new_user(self, name, email, phone_number, password):
        users = self.read_database("u")
        get_user_count = len(users)
        new_user_id = get_user_count + 1
        new_user = User(name, new_user_id, email, phone_number, password)
        users.append(new_user)
        self.total_users = len(users)
        self.write_to_database(users, "u")
        
        return new_user


    #see if userID exists
    def does_user_exist(self, user_id):
        if self.find_user(user_id, None, None) != None:
            return True
        return False
    
    #see if email allready exists
    def find_existing_email(self, email):
        users = self.read_database("u")
        for user in users:
            if user.get_email() == email:
                return True
        return False
    
    # find user and return user-object. will search for all of given arguments, starting with user-id
    # if userid is found the search stops, and returns the object. if not foound moving on to next argument
    # returns None if nothing is found or any argument
    def find_user(self, user_id, user_name, user_email):
        users_list = self.read_database("u")
        user_found = None
        if user_id != None:
            for user in users_list:
                if user.get_user_id() == user_id:
                    user_found = user
                    return user_found
        if user_name != None:
            for user in users_list:
                if user.get_name() == user_name:
                    user_found = user
                    return user_found
        if user_email != None:
            for user in users_list:
                if user.get_email() == user_email:
                    user_found = user
                    return user_found
        
        return user_found
    
    # add ticket-id to user
    def add_ticketid_to_user(self, ticket_id, user_id):
        user_list = self.read_database("u")
        for i in range(len(user_list)):
            if user_list[i].get_user_id() == user_id:
                user_list[i].add_ticket(ticket_id)
                self.write_to_database(user_list, "u")
                return

