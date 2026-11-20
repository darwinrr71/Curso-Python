# Python 30 Días Desktop

Aplicación educativa de escritorio en Python que convierte un manual de estudio de 30 días en una experiencia interactiva local. El proyecto está construido con `tkinter` y organizado para que también sirva como referencia de arquitectura, separación de responsabilidades y buenas prácticas en Python.

## Objetivo pedagógico

La aplicación permite estudiar del día 1 al día 30 con una estructura consistente:

- teoría y objetivo del día
- sintaxis y funcionamiento
- ejemplos y práctica guiada
- errores comunes y buenas prácticas
- ejercicios y mini reto
- código editable y ejecutable dentro de la misma ventana

El contenido base fue extraído del PDF `Manual-python-30-dias.pdf` y reorganizado en carpetas por día dentro de `dias/dia_XX`.

## Stack

- Python 3
- `tkinter` y `ttk` para la interfaz
- `pypdf` para extraer el manual fuente
- `pytest` para pruebas básicas

## Estructura del proyecto

```text
curso/
├── main.py
├── README.md
├── requirements.txt
├── pyproject.toml
├── app/
│   ├── config.py
│   ├── constants.py
│   ├── models/
│   ├── services/
│   ├── ui/
│   └── utils/
├── dias/
│   ├── dia_01/
│   │   ├── lesson.json
│   │   ├── sections/
│   │   ├── examples/
│   │   ├── exercises/
│   │   └── challenge/
│   └── dia_30/
└── tests/
```

## Crear entorno virtual

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
python main.py
```

## Ejecutar en modo desarrollo

```bash
python dev.py
```

Ese modo activa recarga interna de desarrollo: vigila cambios en `main.py`, `app/` y `dias/`, y refresca la interfaz automáticamente dentro de la misma ejecución para que puedas ver ajustes sin relanzar manualmente la app.

Si tu instalación de Python no incluye `Tcl/Tk`, `main.py` mostrará un mensaje claro indicando que debes instalar Python con soporte para `tkinter`.

## Ejecutar tests

```bash
python -m pytest -q
```

## Cómo funciona la app

- `main.py` arranca la ventana principal.
- `app/services/content_loader.py` carga el contenido dinámicamente desde `dias/`.
- `app/services/code_runner.py` ejecuta snippets, captura `stdout`, `stderr` y soporta `input()`.
- `app/ui/main_menu.py` muestra el índice de los 30 días.
- `app/ui/lesson_view.py` presenta la lección en una vista de tres paneles.

## Cómo agregar o modificar un día

1. Crea una carpeta nueva siguiendo el patrón `dias/dia_31` o edita una existente.
2. Mantén un `lesson.json` con metadatos, secciones y bloques de código.
3. Guarda la teoría en `sections/*.md`.
4. Guarda los snippets en `examples/`, `exercises/` y `challenge/`.
5. La app lo cargará dinámicamente si la carpeta sigue la convención `dia_XX`.

## Decisiones técnicas principales

- Se eligió `tkinter` para mantener el proyecto 100% Python y evitar dependencias pesadas.
- El contenido pedagógico vive fuera del motor de UI para facilitar mantenimiento.
- La ejecución de código está encapsulada en un servicio reutilizable.
- La navegación entre días está separada del renderizado.
- El progreso local se guarda en `data/progress.json`.

## Limitaciones conocidas

- Los snippets se ejecutan localmente y comparten el intérprete estándar de Python; no es un sandbox de seguridad fuerte.
- Algunos días orientados a tooling profesional, como `venv`, `pip`, `black` o `ruff`, se muestran con ejemplos Python y comandos documentados, no como automatización del sistema.
- El contenido se extrajo y normalizó desde el PDF, por lo que algunos fragmentos se adaptaron para que fueran ejecutables y consistentes dentro de la app.
