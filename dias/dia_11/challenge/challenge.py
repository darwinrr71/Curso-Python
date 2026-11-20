def subtotal(price, quantity):
    return price * quantity


def discount(subtotal_value, rate):
    return subtotal_value * rate


def total(price, quantity, rate):
    sub = subtotal(price, quantity)
    return sub - discount(sub, rate)


result = total(1.5, 3, 0.0)
print(f"Notebook cuesta {result} y quedan 8 unidades.")
