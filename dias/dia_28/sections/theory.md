Un proyecto real no se empieza escribiendo líneas al azar. Primero se diseña.

Qué hará el proyecto

agregar tareas, listar tareas, marcar tareas como completadas, eliminar tareas, guardar en JSON, cargar desde JSON, organizar código en varios módulos.

Estructura sugerida

project/ main.py models.py storage.py services.py tests/ test_services.py tasks.json

Diseño de modelo

Usaremos dataclass para representar una tarea.
