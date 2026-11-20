numbers = [3, 1, 2]
print(sorted(numbers))
values = [True, False, True]
print(any(values))
print(all(values))
users = [
    {"name": "Ana", "age": 30},
    {"name": "Luis", "age": 25},
]

ordered = sorted(users, key=lambda user: user["age"])
print(ordered)
