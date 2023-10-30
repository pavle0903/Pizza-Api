import requests
import time
import getpass
import os

#baseUrl = 'http://0.0.0.0:8000'
baseUrl = 'http://127.0.0.1:8000'

def register_user(username, password):
    #url = 'http://0.0.0.0:8000/register'
    data = {'username': username, 'password': password}
    response = requests.post(baseUrl + "/register", json=data)

    if response.status_code == 201:
        print(f"Registration successful for user {username}!")
        login_user()
    elif response.status_code == 409:
        print("Username is already taken. Please choose a different username.")
    else:
        print(f"Error: {response.json().get('error')}")

def login_user():
    print("Loading login screen..")
    time.sleep(0.5)
    logged_in=False
    while not logged_in:

        username = input('Enter username: ')
        password = input('Enter your password: ')

        data = {'username': username, 'password': password}
        response = requests.post(baseUrl + "/login", json=data)
        time.sleep(1)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            role = response.json().get('role')
            if access_token:
                os.environ['JWT_TOKEN'] = access_token
            else:
                print("Invalid server response")
            print(f"Welcome {username}! You are successfully logged in!")
            logged_in = True
            #time.sleep(1)
            get_logged_user()
        elif response.status_code == 409:
            print("Invalid credentials. Please check your username and password.")
        else:
            print(f"Error: {response.json().get('error')}")
            return None, None

def get_logged_user():
    response = requests.get(baseUrl + "/get_logged_user")
   

    if response.status_code == 200:
        user = response.json()
        print(user)
        if user['role'] == 'admin':

            access_token = os.environ.get('JWT_TOKEN')
            if access_token:
                headers = {'Authorization': f'Bearer {access_token}'}
                response = requests.get(f'{baseUrl}/admin_menu', headers=headers)

                if response.status_code == 200:

                    admin_menu(access_token)
                else:
                    print(f"Error accessing admin menu: {response.json().get('error')}")
            else:
                print("JWT_TOKEN not found in the environment. Please log in first.")
        else:

            menu_list(user)

    elif response.status_code == 404:
        print("There is no logged-in user")
    else:
        print(f"Error: {response.json().get('error')}")

def admin_menu(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    while True:
        print("1. Add pizza to the menu")
        print("2. Delete pizza from the menu")
        print("3. Cancel order")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_pizza()
        
        if choice == '2':
            delete_pizza()
        else:
            print("Invalid choice. Try again!")

def create_pizza():
    pizza_name = input("Enter pizza name: ")
    pizza_desc = input("Enter pizza description: ")
    pizza_price = input("Enter pizza price: ")

    create_pizza = {'name': pizza_name, 'description': pizza_desc, 'price': pizza_price}

    response = requests.post(baseUrl + "/create_pizza", json=create_pizza, headers=headers)

    if response.status_code == 201:
        print(f"Successfully added pizza {pizza_name}!")
    else:
        print(f"Error: {response.json().get('error')}")

def delete_pizza():
    response1 = requests.get(baseUrl + "/get_pizzas")

    if response1.status_code == 200:
        pizza_list = response1.json().get('pizzas')
        #counter = 0
        print("Menu: ")
        for pizza in pizza_list:
            print(f"{pizza['id']}. " + pizza['name'])
    else:
        print(f'Error: {response1.status_code}')

    id = input("Enter the pizza ID you would like to delete: ")

    response = requests.delete(baseUrl + f"/delete_pizza/{id}", headers=headers)

    if response.status_code == 200:
        
        print("Pizza is successfully deleted from the menu!")
    else:
        print("Pizza number does not exists!", f'{response.status_code}')


def menu_list(user):
    while True:
        print("1. Create order")
        print("2. Check order status")
        print("3. Cancel order")

        choice = input("Enter your choice: ")

        if choice == '1':
            response = requests.get(baseUrl + "/get_pizzas")

            if response.status_code == 200:
                pizza_list = response.json().get('pizzas')
                #counter = 0
                print("Menu: ")
                for pizza in pizza_list:
                    print(f"{pizza['id']}. " + pizza['name'])
            else:
                print(f'Error: {response.status_code}')

            pizza_choice = int(input("Enter the number of the pizza you would like to order: "))
            selected_pizza = next((pizza for pizza in pizza_list if pizza['id'] == pizza_choice), None)
            
            if selected_pizza:
                print(f"You selected {selected_pizza['name']}. The price is: {selected_pizza['price']}")
            else:
                print("Invalid selection. Please enter the valid ID.")

            create_order(user, selected_pizza)


        
        elif choice == '2':
            #order_choice = input("Enter your order ID to check status: ")
            response = requests.get(baseUrl + f"/get_orders/{user['username']}")
            if response.status_code == 200:

                orders = response.json().get('orders')
                print('Loading your orders..')
                time.sleep(0.3)
                print('====== ORDERS ======')
                for order in orders:
                    print(f"Order number: {order['id']}, {order['pizza']}, price: {order['price']}, status: {order['status']}")
                print('====================')
                time.sleep(0.3)
            else:
                print("You dont have any orders yet!")
            #print(orders)
        
        elif choice == '3':
            cancel_choice = input("Enter your order ID to cancel: ")

            response = requests.delete(baseUrl + f"/cancel_order/{user['username']}/{cancel_choice}")

            if response.status_code == 200:
                print("Your order has been successfully canceled!")
            else:
                print(f"Invalid order number. Try again. ({response.status_code})")

        else:
            print("Invalid choice. Try again!")
    
def create_order(user, pizza):
    data = {'username': user['username'], 'pizza': pizza}
    response = requests.post(baseUrl + "/make_order", json=data)

    if response.status_code == 201:
        print(f'Order is successfully created!')
    else:
        print(f"Error: {response.status_code}")



if __name__ == '__main__':
    username = input('Enter username: ')
    password = input('Enter password: ')

    register_user(username, password)