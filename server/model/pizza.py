class Pizza:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __json__(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price}