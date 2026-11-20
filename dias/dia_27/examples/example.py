def calculate_total(price: float, quantity: int) -> float:
    subtotal = price * quantity
    tax = subtotal * 0.08
    return subtotal + tax


print(calculate_total(10.0, 5))
