class Animal:
def speak(self):
print("Some sound")
class Dog(Animal):
def speak(self):
print("Woof")

Composición

class Engine:
def start(self):
print("Engine started")
class Car:
def __init__(self):
self.engine = Engine()
