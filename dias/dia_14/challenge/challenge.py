activities = [
    ("Practice", 1),
    ("Study", 2),
    ("Rest", 3),
]

ordered = sorted(activities, key=lambda item: item[1])
print(f"{ordered[0][0]} {ordered[0][1]}")
