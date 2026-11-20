Archivo utils.py

def is_even(number):
    return number % 2 == 0


Archivo main.py

from utils import is_even

print(is_even(10))
