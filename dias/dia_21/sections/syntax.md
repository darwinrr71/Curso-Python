import requests

response = requests.get("https://api.example.com/users")
print(response.status_code)
print(response.json())
