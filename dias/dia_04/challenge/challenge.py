price = float(input("Price: "))
vip = input("VIP customer? (yes/no): ").strip().lower()

if price >= 50 or vip == "yes":
    print("Envío gratis")
else:
    print("Envío estándar")
