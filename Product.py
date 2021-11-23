class Product:
    def __init__(self, name, quantity, description=None):
        self.description = description
        self.quantity = quantity
        self.name = name

    def __dict__(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "description": self.description
        }
