from model.order import Order
from flask import jsonify

class OrderManager:
    def __init__(self):
        self.orders = []
        self.order_id = 0
        # self.orders.append(Order(0, 'nikola', 'neka pica', 30, 'not ready'))
        # self.orders.append(Order(2, 'petar', 'neka pica', 30, 'not ready'))
        # self.orders.append(Order(3, 'marija', 'neka pica', 30, 'not ready'))

    def make_order(self, user, pizza, price, status='Not ready'):

        new_order = Order(self.order_id, user, pizza, price, status)
        self.order_id+=1
        self.orders.append(new_order)

        return new_order
    
    def get_orders(self, username):
        print(self.orders)
        return [order.__json__() for order in self.orders if order.user == username]
    
    def cancel_order(self, username, order_id):
        for order in self.orders:
            if order.id == int(order_id) and order.user == username:
            
                self.orders.remove(order)
                
                return self.orders
            else:
                return None
       