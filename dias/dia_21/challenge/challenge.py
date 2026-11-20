users = [{"name": "Ada", "active": True}, {"name": "Grace", "active": False}]
active_users = [user["name"] for user in users if user["active"]]
print(active_users)
