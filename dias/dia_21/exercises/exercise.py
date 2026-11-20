response = {
    "status_code": 200,
    "data": {"name": "Ana", "active": True},
}

if response["status_code"] == 200:
    print(response["data"]["name"])
