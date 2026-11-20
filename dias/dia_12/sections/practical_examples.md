Buen uso de locales

def calculate_total(price, quantity):
    subtotal = price * quantity
    return subtotal


Evitar depender demasiado de globales

TAX_RATE = 0.25

def add_tax(price):
    return price * (1 + TAX_RATE)
