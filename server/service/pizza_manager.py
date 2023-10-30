from model.pizza import Pizza
from flask import jsonify

class PizzaManager():
    def __init__(self):
        self.pizzas = []
        
        pizza1 = Pizza(0, 'Capricciosa pizza', 'Such a good pizza', 20)
        pizza2 = Pizza(1, 'Margherita pizza', "The best pizza", 30)
        pizza3 = Pizza(2, 'Pepperoni pizza', 'Not bad pizza', 40)
        self.pizzas.append(pizza1)
        self.pizzas.append(pizza2)
        self.pizzas.append(pizza3)

        self.next_pizza_id = 0

    def add_pizza(self, pizza_data):
        pizza_id = self.next_pizza_id +1

        pizza = Pizza(pizza_id, name=pizza_data['name'], description=pizza_data['description'], price=pizza_data['price'])
        self.pizzas.append(pizza)
        print(self.pizzas)
        return pizza
    
    def get_pizzas(self):
        return [pizza.__json__() for pizza in self.pizzas]