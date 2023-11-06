from flask import jsonify
from service.order_manager import OrderManager

class OrderHandler:
    def __init__(self):
        self.order_manager = OrderManager()

    def make_order(self, data):
        user = data.get('username')
        pizza = data.get('pizza')

        add_order = self.order_manager.make_order(user, pizza['name'], pizza['price'])

        if add_order:
            return jsonify({'message': f'Order has been created!'}), 201
            
        else:
            return jsonify({'message': 'Order could not be completed. Try again!'}), 409
        
    def get_user_orders(self, user):
        orders = self.order_manager.get_orders(user)

        if orders:
            return jsonify({'orders': orders}), 200
        else:
            return jsonify({'message': 'Orders not found'}), 404
        
    def get_all_orders(self):
        orders = self.order_manager.get_all_orders()

        if orders:
            return jsonify({'orders': orders}), 200
        else:
            return jsonify({'message': 'Orders not found'}), 404
        
    def user_cancel_order(self, username, order_id):
        cancel_order = self.order_manager.cancel_order(username, order_id)

        return jsonify({'message': cancel_order[0],}), cancel_order[1]
    
        # if cancel_order[1] == 200:
        #     return jsonify({'message': 'Order has been successfully canceled!'}), 200
        # elif cancel_order is False:
        #     return jsonify({'message': 'Order cancel could not be completed!'}), 404
        # elif cancel_order is True:
        #     return jsonify({'message': 'Order can not be canceled since its order is ready!'}), 403

    def admin_cancel_order(self, order_id):
        cancel_order = self.order_manager.admin_cancel_order(order_id)

        if cancel_order is not None:
            return jsonify({'message': 'Order has been successfully canceled!'}), 200
        else:
            return jsonify({'message': 'Order cancel could not be completed!'}), 404