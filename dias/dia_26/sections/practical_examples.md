Probar una función de descuento

def calculate_discount(price, percent):
    return price * percent


Test:

from discounts import calculate_discount


def test_calculate_discount():
    assert calculate_discount(100, 0.1) == 10
