'''
This module is for all functions that do operations on the User-objects.
'''
from classes import User

users = []

def addNewUser(name, userName, email, password):
    users.append(User(name, userName, users.count()+1, email, password))