Guardar configuración

settings = {

"theme": "dark",

"language": "es", "notifications": True, }

Leer tareas

with open("tasks.json", "r", encoding = "utf - 8") as file:
tasks = json.load(file)
