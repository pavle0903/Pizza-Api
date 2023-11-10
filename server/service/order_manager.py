from model.order import Order
import threading
import time
from flask import jsonify

class OrderManager:
    def __init__(self):
        self.orders = []
        self.order_id = 0

    def make_order(self, user, pizza, price, status='Not ready'):

        new_order = Order(self.order_id, user, pizza, price, status)
        self.order_id+=1
        self.orders.append(new_order)

        threading.Thread(target=self.delayed_status_change, args=(new_order,), daemon=True).start()
        
        return new_order
    
    def delayed_status_change(self, order):
        time.sleep(15)
        order.status = 'Ready to be delivered'
        print(f"Order {order.id} is now ready to be delivered.")
    
    def get_orders(self, username):
        print(self.orders)
        return [order.__json__() for order in self.orders if order.user == username]

    def get_all_orders(self):
        print(self.orders)
        return [order.__json__() for order in self.orders]
    
    def cancel_order(self, username, order_id):
        
        if not self.orders:
            return ("There is no orders at this moment!", 404)
        else:
            for order in self.orders:
                if order.id == int(order_id) and order.user == username:
                    if order.status != 'Ready to be delivered':
                        self.orders.remove(order)
                        return ("Successfully canceled", 200)
                    else:
                        return ("Your order status is ready to be delivered, cannot be canceled!", 403)
                else:
                    return ("Invalid id. Cannot be deleted", 404)
        
                
            
    def admin_cancel_order(self, order_id):
        for order in self.orders:
            if order.id == int(order_id):
            
                self.orders.remove(order)
                
                return self.orders
            else:
                return None
       