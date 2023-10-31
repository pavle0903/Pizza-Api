import json
from dotenv import load_dotenv
import os
from service.user_manager import UserManager
from service.pizza_manager import PizzaManager
from service.order_manager import OrderManager
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity,get_jwt

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

jwt = JWTManager(app)

pizza_manager = PizzaManager()
user_manager = UserManager()
order_manager = OrderManager()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    new_user = user_manager.register_user(username, password)

    if new_user:
        return jsonify({'message': f'Successful registration for user {new_user.username}'}), 201
    else:
        return jsonify({'message': 'Username already taken. Please choose a different username'}), 409

@app.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    login_user = user_manager.login(username, password)

    if login_user:
        if login_user.role == 'admin':
            access_token = create_access_token(identity=username, additional_claims={'role': login_user.role})
            return jsonify(access_token=access_token, role=login_user.role), 200
        else:
            return jsonify({'message': f'Successful login for user {login_user.username}'}), 200
    else:
        return jsonify({'message': 'Provided credentials are not found. Please try again!'}), 409

    # if login_user:
    #     return jsonify({'message': f'Successful login for user {login_user.username}'}), 200
    # else:
    #     return jsonify({'message': 'Provided credentials are not found. Please try again!'}), 409
    
@app.route('/get_logged_user', methods=['GET'])
def get_logged_user():
    logged_user = user_manager.get_logged_user()
    #print("printam na serveru usera", logged_user)
    return jsonify(logged_user)

@app.route('/create_pizza', methods=['POST'])
@jwt_required()
def create_pizza():
    current_user = get_jwt_identity()
    user_role = get_jwt().get('role')

    if user_role == 'admin':

        data = request.get_json()
        add_pizza = pizza_manager.add_pizza(data)

        if add_pizza:
            return jsonify({'message' : f'Pizza added to menu'}), 201
        else:
            return jsonify({'message': 'Pizza creating could not be completed. Try again!'}), 409
    else:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route('/get_pizzas', methods=['GET'])
def get_pizzas():
    get_pizzas = pizza_manager.get_pizzas()

    print(get_pizzas, "ovo su pice u get pizzas na srv")

    return jsonify({'pizzas' : get_pizzas})

@app.route('/make_order', methods=['POST'])
def make_order():
    data = request.get_json()
    user = data.get('username')
    pizza = data.get('pizza')

    add_order = order_manager.make_order(user, pizza['name'], pizza['price'])

    if add_order:
        return jsonify({'message': f'Order has been created!'}), 201
        
    else:
        return jsonify({'message': 'Order could not be completed. Try again!'}), 409

@app.route('/get_orders/<user>', methods=['GET'])
def get_orders(user):
    orders = order_manager.get_orders(user)
    print(orders)

    if orders:
        return jsonify({'orders': orders}), 200
    else:
        return jsonify({'message': 'Orders not found'}), 404
    
@app.route('/get_orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    user_role = get_jwt().get('role')

    if user_role == 'admin':
        orders = order_manager.get_all_orders()
        print(orders)

        if orders:
            return jsonify({'orders': orders}), 200
        else:
            return jsonify({'message': 'Orders not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    
@app.route('/cancel_order/<username>/<order_id>', methods=['DELETE'])
def cancel_order(username, order_id):
    cancel_order = order_manager.cancel_order(username, order_id)

    return jsonify({'message': cancel_order[0],}), cancel_order[1]

    # if cancel_order[1] == 200:
    #     return jsonify({'message': 'Order has been successfully canceled!'}), 200
    # elif cancel_order is False:
    #     return jsonify({'message': 'Order cancel could not be completed!'}), 404
    # elif cancel_order is True:
    #     return jsonify({'message': 'Order can not be canceled since its order is ready!'}), 403

    
@app.route('/cancel_order/<order_id>', methods=['DELETE'])
@jwt_required()
def admin_cancel_order(order_id):
    user_role = get_jwt().get('role')

    if user_role == 'admin':
        cancel_order = order_manager.admin_cancel_order(order_id)

        if cancel_order is not None:
            return jsonify({'message': 'Order has been successfully canceled!'}), 200
        else:
            return jsonify({'message': 'Order cancel could not be completed!'}), 404

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
        delete = pizza_manager.delete_pizza(pizza_id)
        if delete:
            return jsonify({'message': 'Pizza is successfully deleted from the menu!'}), 200
        else:
            return jsonify({'message': 'Pizza ID does not exists'}), 404
    else:
        return jsonify({'message': "Unauthorized action!"}), 401


if __name__ == '__main__':
    app.run(port=8000)