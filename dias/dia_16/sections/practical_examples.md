Escribir archivo

with open("hello.txt", "w", encoding="utf-8") as file:
    file.write("Hello, Python\n")

Leer líneas

with open("hello.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
