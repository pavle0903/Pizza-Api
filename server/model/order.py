class Order:
    def __init__(self, id, user, pizza, price, status):
        self.id = id
        self.user = user
        self.pizza = pizza
        self.status = status
        self.price = price

    def __json__(self):
        return {'id': self.id, 'user': self.user, 'pizza': self.pizza, 'status': self.status, 'price': self.price}