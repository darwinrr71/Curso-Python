Consultar datos

import requests

url = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(url, timeout=10)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Request failed")
