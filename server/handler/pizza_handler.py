from service.pizza_manager import PizzaManager
from flask import jsonify

class PizzaHandler:
    def __init__(self):
        self.pizza_manager = PizzaManager()

    def create_pizza(self, data):
        print(data, "ovo je data u handleru create pizza")
        add_pizza = self.pizza_manager.add_pizza(data)

        if add_pizza:
            print(add_pizza)
            print(self.pizza_manager.pizzas)
            return jsonify({'message' : f'Pizza added to menu'}), 201
        else:
            return jsonify({'message': 'Pizza creating could not be completed. Try again!'}), 409
        
    def get_pizzas(self):
        get_pizzas = self.pizza_manager.get_pizzas()

        return jsonify({'pizzas' : get_pizzas})
    

    def delete_pizza(self, pizza_id):
        delete = self.pizza_manager.delete_pizza(pizza_id)
        if delete:
            return jsonify({'message': 'Pizza is successfully deleted from the menu!'}), 200
        else:
            return jsonify({'message': 'Pizza ID does not exists'}), 404

