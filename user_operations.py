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
        for user in self.users:
            if user.get_user_id() == user_id:
                return True
        return False
    
    #see if email allready exists
    def find_existing_email(self, email):
        for user in self.users:
            if user.get_email() == email:
                return True
        return False
    
    # find user and return user-object. will search for all of given arguments, starting with user-id
    # if userid is found the search stops, and returns the object. if not foound moving on to next argument
    # returns None if nothing is found or any argument
    def find_user(self, user_id, user_name, user_email):
        user_found = None
        if user_id != None:
            for user in self.users:
                if user.get_user_id() == user_id:
                    user_found = user
                    return user_found
        if user_name != None:
            for user in self.users:
                if user.get_name() == user_name:
                    user_found = user
                    return user_found
        if user_email != None:
            for user in self.users:
                if user.get_email() == user_email:
                    user_found = user
                    return user_found
        
        return user_found
    
    # reset game, moving all active tickets to archived and clearing active tickets
    def reset_game(self):
        for user in self.users:
            user.move_active_to_archived()
            user.clear_active_tickets()
