def add_all(*args):
    total = 0
    for number in args:
        total += number
    return total


def show_user(**kwargs):
    print(kwargs)


numbers = [10, 20]
print(*numbers)
