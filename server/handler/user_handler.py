from flask import Flask, request, jsonify
from service.user_manager import UserManager
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity,get_jwt

class UserHandler:
    def __init__(self):
        
        self.user_manager = UserManager()

    def register_user(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        new_user = self.user_manager.register_user(username, password)
        
        if new_user:
            return jsonify({'message': f'Successful registration for user {new_user.username}'}), 201
        else:
            return jsonify({'message': 'Username already taken. Please choose a different username'}), 409
    
    def login_user(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        login_user = self.user_manager.login(username, password)

        if login_user:
            if login_user.role == 'admin':
                access_token = create_access_token(identity=username, additional_claims={'role': login_user.role})
                return jsonify(access_token=access_token, role=login_user.role), 200
            else:
                return jsonify({'message': f'Successful login for user {login_user.username}'}), 200
        else:
            return jsonify({'message': 'Provided credentials are not found. Please try again!'}), 409
        
    def get_logged_user(self):
        logged_user = self.user_manager.get_logged_user()

        return jsonify(logged_user)