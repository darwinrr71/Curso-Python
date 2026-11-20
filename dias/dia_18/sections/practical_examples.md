División segura

try:
    a = int(input("A: "))
    b = int(input("B: "))
    result = a / b
except ValueError:
    print("You must enter valid integers")
except ZeroDivisionError:
    print("You cannot divide by zero")
else:
    print(result)
