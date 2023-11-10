import requests
import time
import sys
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
        time.sleep(0.4)
        login_user()
    elif response.status_code == 409:
        print("Username is already taken. Please choose a different username.")
        time.sleep(0.4)
    else:
        print(f"Error: {response.json().get('error')}")

def login_user():
    print("Loading login screen..")
    time.sleep(0.3)
    logged_in=False
    while not logged_in:
        print("------ LOGIN SCREEN ------")
        username = input('Enter username: ')
        password = getpass.getpass('Enter your password: ')

        data = {'username': username, 'password': password}
        response = requests.post(baseUrl + "/login", json=data)
        time.sleep(1)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            role = response.json().get('role')
            if access_token:
                os.environ['JWT_TOKEN'] = access_token
            # else:
            #     print("Invalid server response")
            print(f"Welcome {username}! You are successfully logged in!")
            logged_in = True
            time.sleep(0.4)
            get_logged_user()
        elif response.status_code == 409:
            print("Invalid credentials. Please check your username and password.")
            time.sleep(0.4)
        else:
            print(f"Error: {response.json().get('error')}")
            return None, None

def get_logged_user():
    response = requests.get(baseUrl + "/get_logged_user")
   

    if response.status_code == 200:
        user = response.json()
        
        if user['role'] == 'admin':

            access_token = os.environ.get('JWT_TOKEN')
            if access_token:
                headers = {'Authorization': f'Bearer {access_token}'}
                response = requests.get(f'{baseUrl}/admin_menu', headers=headers)

                if response.status_code == 200:
                    time.sleep(0.4)
                    admin_menu(access_token)
                else:
                    print(f"Error accessing admin menu: {response.json().get('error')}")
                    time.sleep(0.4)
            else:
                print("JWT_TOKEN not found in the environment. Please log in first.")
                time.sleep(0.4)
        else:
            time.sleep(0.4)
            menu_list(user)

    elif response.status_code == 404:
        print("There is no logged-in user")
    else:
        print(f"Error: {response.json().get('error')}")

def admin_menu(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    print("Loading admin menu..")
    time.sleep(0.3)
    while True:
        print("------ ADMIN MENU ------")
        print("1. Add pizza to the menu")
        print("2. Delete pizza from the menu")
        print("3. Cancel order")
        print("4. Show menu")
        print("5. Logout")
        print("------------------------")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_pizza(headers)
            time.sleep(0.4)
        
        elif choice == '2':
            delete_pizza(headers)
            time.sleep(0.4)
        
        elif choice == '3':
            cancel_order(headers)
            time.sleep(0.4)
        elif choice == '4':
            show_menu()
            time.sleep(0.4)
        elif choice == '5':
            break

        else:
            print("Invalid choice. Try again!")
            time.sleep(0.4)

def show_menu():
    response1 = requests.get(baseUrl + "/get_pizzas")
    time.sleep(0.5)
    if response1.status_code == 200:
        pizza_list = response1.json().get('pizzas')
        #counter = 0
        if not pizza_list:
            print("There is no pizzas on the menu!")
        else:
            print("------ PIZZA MENU ------")
            for pizza in pizza_list:
                print(f"{pizza['id']}. " + pizza['name'])
            print("------------------------")
    time.sleep(0.5)
    return response1
       

def cancel_order(headers):
    response1 = requests.get(baseUrl + f"/get_orders", headers=headers)
    if response1.status_code == 200:

        orders = response1.json().get('orders')
        print('------ ORDERS ------')
        for order in orders:
            print(f"Order number: {order['id']}, customer: {order['user']}, {order['pizza']}, price: {order['price']}, status: {order['status']}")
        print('--------------------')

        cancel_choice = input("Enter order ID to cancel: ")

        response = requests.delete(baseUrl + f"/cancel_order/{cancel_choice}", headers=headers)

        if response.status_code == 200:
            print("Order has been successfully canceled!")
        else:
            print(f"Invalid order number. Try again. ({response.status_code})")
    else:
        print("There is no orders at this moment!")

def create_pizza(headers):
    pizza_name = input("Enter pizza name: ")
    pizza_desc = input("Enter pizza description: ")
    pizza_price = input("Enter pizza price: ")

    create_pizza = {'name': pizza_name, 'description': pizza_desc, 'price': pizza_price}

    response = requests.post(baseUrl + "/create_pizza", json=create_pizza, headers=headers)

    if response.status_code == 201:
        print(f"Successfully added pizza {pizza_name}!")
    else:
        print(f"Error: {response.json().get('error')}")

def delete_pizza(headers):
    # response1 = requests.get(baseUrl + "/get_pizzas")

    # if response1.status_code == 200:
    #     pizza_list = response1.json().get('pizzas')
    #     #counter = 0
    #     if not pizza_list:
    #         print("There is no pizzas on menu!")
    #     else:
    #         print("------ MENU ------")
    #         for pizza in pizza_list:
    #             print(f"{pizza['id']}. " + pizza['name'])
    #         print("------------------")
    response1 = show_menu()
    if response1:
        
        id = input("Enter the pizza ID you would like to delete: ")

        response = requests.delete(baseUrl + f"/delete_pizza/{id}", headers=headers)

        if response.status_code == 200:
            
            print("Pizza is successfully deleted from the menu!")
        else:
            print("Pizza number does not exists!", f'{response.status_code}')
    else:
        print(f'Error: {response1.status_code}')


def menu_list(user):
    while True:
        print("------ MENU ------")
        print("1. Create order")
        print("2. Check order status")
        print("3. Cancel order")
        print("4. Show menu")
        print("5. Logout")
        print("------------------")

        choice = input("Enter your choice: ")

        if choice == '1':
            response = show_menu()
            pizza_list = response.json().get('pizzas')
            if pizza_list:
                pizza_choice = int(input("Enter the number of the pizza you would like to order: "))
                selected_pizza = next((pizza for pizza in pizza_list if pizza['id'] == pizza_choice), None)
                
                if selected_pizza:
                    print(f"You selected {selected_pizza['name']}. The price is: {selected_pizza['price']}")
                    time.sleep(0.3)
                    create_order(user, selected_pizza)
                else:
                    print("Invalid selection. Please enter the valid ID.")
                    time.sleep(0.4)
            else:
                
                time.sleep(0.4)
                break


        
        elif choice == '2':
            #order_choice = input("Enter your order ID to check status: ")
            response = requests.get(baseUrl + f"/get_orders/{user['username']}")
            if response.status_code == 200:

                orders = response.json().get('orders')
                print('Loading your orders..')
                time.sleep(0.3)
                print('------ YOUR ORDERS ------')
                for order in orders:
                    print(f"Order number: {order['id']}, {order['pizza']}, price: {order['price']}, status: {order['status']}")
                print('-------------------------')
                time.sleep(0.3)
            else:
                print("You do not have any orders yet!")
                time.sleep(0.3)
            #print(orders)
        
        elif choice == '3':
            cancel_choice = input("Enter your order ID to cancel: ")

            response = requests.delete(baseUrl + f"/cancel_order/{user['username']}/{cancel_choice}")

            if response.status_code == 200:
                print("Your order has been successfully canceled!")
                time.sleep(0.4)

            elif response.status_code == 403:
                print("Your order status is ready! Cannot be canceled!")
                time.sleep(0.4)
            else:
                print(f"Invalid order number. Try again. ({response.status_code})")
                time.sleep(0.4)

        elif choice == '4':
            response = show_menu()
            
        elif choice == '5':
            break

        else:
            print("Invalid choice. Try again!")
            time.sleep(0.4)
    
def create_order(user, pizza):
    data = {'username': user['username'], 'pizza': pizza}
    response = requests.post(baseUrl + "/make_order", json=data)

    if response.status_code == 201:
        print(f'Order is successfully created!')
        time.sleep(0.3)
    else:
        print(f"Error: {response.status_code}")

def reg_log_menu():
    while True:
        print("------ REGISTRATION/LOGIN MENU ------")
        print("1. Register your account")
        print("2. Log into your account")
        print("3. Exit")
        print("-------------------------------------")

        choice = input("Enter your choice: ")

        if choice == '1':
            time.sleep(0.3)
            print("------ REGISTRATION SCREEN ------")
            username = input('Enter username: ')
            password = getpass.getpass('Enter your password: ')
            register_user(username, password)
        elif choice == '2':
            login_user()
        elif choice == '3':
            sys.exit()
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    reg_log_menu()