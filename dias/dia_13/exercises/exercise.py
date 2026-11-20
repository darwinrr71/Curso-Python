students = ["Ana", "Luis", "Eva"]
grades = [8, 7, 9]

for index, (student, grade) in enumerate(zip(students, grades), start=1):
    print(index, student, grade)
