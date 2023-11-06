import json
from dotenv import load_dotenv
import os
from service.user_manager import UserManager
from service.pizza_manager import PizzaManager
from service.order_manager import OrderManager
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity,get_jwt

from handler.user_handler import UserHandler
from handler.pizza_handler import PizzaHandler
from handler.order_handler import OrderHandler


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

jwt = JWTManager(app)

user_handler = UserHandler()
pizza_handler = PizzaHandler()
order_handler = OrderHandler()

pizza_manager = PizzaManager()
user_manager = UserManager()
order_manager = OrderManager()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return user_handler.register_user(data)
    
    
@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    return user_handler.login_user(data)

    # if login_user:
    #     return jsonify({'message': f'Successful login for user {login_user.username}'}), 200
    # else:
    #     return jsonify({'message': 'Provided credentials are not found. Please try again!'}), 409
    
@app.route('/get_logged_user', methods=['GET'])
def get_logged_user():
    # logged_user = user_manager.get_logged_user()
    # #print("printam na serveru usera", logged_user)
    # return jsonify(logged_user)
    return user_handler.get_logged_user()

@app.route('/create_pizza', methods=['POST'])
@jwt_required()
def create_pizza():
    current_user = get_jwt_identity()
    user_role = get_jwt().get('role')

    if user_role == 'admin':
        data = request.get_json()
        
        return pizza_handler.create_pizza(data)
    else:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/get_pizzas', methods=['GET'])
def get_pizzas():
    return pizza_handler.get_pizzas()

@app.route('/make_order', methods=['POST'])
def make_order():
    data = request.get_json()
    return order_handler.make_order(data)

@app.route('/get_orders/<user>', methods=['GET'])
def get_orders(user):
    return order_handler.get_user_orders(user)
    
@app.route('/get_orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    user_role = get_jwt().get('role')

    if user_role == 'admin':
        return order_handler.get_all_orders()
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    
@app.route('/cancel_order/<username>/<order_id>', methods=['DELETE'])
def cancel_order(username, order_id):

    return order_handler.user_cancel_order(username, order_id)
    
@app.route('/cancel_order/<order_id>', methods=['DELETE'])
@jwt_required()
def admin_cancel_order(order_id):
    user_role = get_jwt().get('role')

    if user_role == 'admin':
        return order_handler.admin_cancel_order(order_id)
    else:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/admin_menu', methods=['GET'])
@jwt_required()
def admin_menu():
    current_user = get_jwt_identity()
    user_role = get_jwt().get('role')

    if user_role == 'admin':
        return jsonify(message=f'Welcome, {current_user}! You have access to the admin menu.'), 200
    else:
        return jsonify({'error': 'Unauthorized access'}), 401
    
@app.route('/delete_pizza/<pizza_id>', methods=['DELETE'])
@jwt_required()
def delete_pizza(pizza_id):
    user_role = get_jwt().get('role')
    if user_role == 'admin':
        return pizza_handler.delete_pizza(pizza_id)
    else:
        return jsonify({'message': "Unauthorized action!"}), 401


if __name__ == '__main__':
    app.run(port=8000)