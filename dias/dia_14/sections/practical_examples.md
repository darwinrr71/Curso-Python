Verificar emails no vacíos

emails = ["a@test.com", "b@test.com", ""]
print(all(emails))

Ordenar productos por precio

products = [
    {"name": "Mouse", "price": 20},
    {"name": "Laptop", "price": 900},
]

ordered = sorted(products, key=lambda item: item["price"])
print(ordered)
