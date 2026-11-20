Clase Product

class Product:
def __init__(self, name, price):
self.name = name
self.price = price
def apply_discount(self, percentage):
self.price = self.price* (1 - percentage)
