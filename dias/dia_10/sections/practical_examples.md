Buscar elemento

names = ["Ana", "Luis", "Sofía"]

for name in names:
    if name == "Luis":
        print("Found")
        break

Saltar números pares

for i in range(10):
    if i % 2 == 0:
        continue
    print(i)
