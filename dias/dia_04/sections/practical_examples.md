Sistema de acceso

username = input("Username: ")
if username == "admin":
    print("Access granted")
else:
    print("Access denied")

Clasificación por nota

grade = float(input("Grade: "))

if grade >= 9:
    print("Excellent")
elif grade >= 7:
    print("Good")
elif grade >= 5:
    print("Pass")
else:
    print("Fail")
