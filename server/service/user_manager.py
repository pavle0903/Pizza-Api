from model.users import User
from flask import jsonify

class UserManager():
    def __init__(self):
        self.users = []
        self.logged_user = None
        admin = User('admin', 'admin','admin')
        self.users.append(admin)

    def register_user(self, username, password, role='customer'):

        if self.find_user(username):
            print("User with provided username already exists")
            return None

        new_user = User(username, password, role)
        self.users.append(new_user)
        return new_user

    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
        
    def login(self, username, password):
        user = self.find_user(username)
        if user and user.password == password:
            self.logged_user = user
            
            return user
        return None
    
    def get_logged_user(self):
        if self.logged_user:
            return {'username' : self.logged_user.username, 'role': self.logged_user.role}
        else:
            return {'message' : 'No user is currently logged in!'}