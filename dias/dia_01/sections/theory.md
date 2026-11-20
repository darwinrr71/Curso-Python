Qué es Python

Python es un lenguaje de programación de alto nivel, multiparadigma y de propósito general. “De alto nivel” significa que su sintaxis está más cerca del lenguaje humano que del lenguaje máquina. “Multiparadigma” significa que soporta distintos estilos de programación, como programación imperativa,

orientada a objetos y funcional. “De propósito general” significa que se puede usar para muchas áreas: automatización, backend, scripts, análisis de datos, testing, herramientas internas, APIs y más. Python se hizo muy popular porque prioriza la legibilidad. Es un lenguaje que intenta que el código sea claro y fácil de mantener. Eso se nota en decisiones como la indentación obligatoria o una sintaxis generalmente simple.

Cómo se ejecuta Python

Cuando escribes código Python en un archivo.py, normalmente lo ejecutas con el intérprete de Python. Un intérprete es el programa que lee tu código y lo ejecuta.

Ejemplo de archivo:

print("Hola, Python")

Si guardas ese archivo como main.py, puedes ejecutarlo desde terminal así:

python main.py

O en algunos sistemas:

python3 main.py

Qué es un archivo .py

Un archivo.py es simplemente un archivo de texto que contiene código Python. No tiene nada mágico por sí mismo. La extensión.py indica que su contenido debe interpretarse como código Python.

Qué hace print()

print() es una función incorporada de Python que muestra información en la salida estándar ,

normalmente la terminal.

Es muy útil para:

ver resultados, depurar, entender cómo va cambiando el programa, mostrar mensajes al usuario.

Qué es una variable

Una variable es un nombre que hace referencia a un valor. En Python no declaras variables con una palabra como int, let o String. Simplemente asignas un valor con =.

name = "Ana"
age = 30

Aquí name apunta al valor "Ana" y age apunta al valor 30.

Tipado dinámico

Python es un lenguaje de tipado dinámico. Eso significa que no necesitas declarar explícitamente el tipo de una variable al crearla. El tipo está en el valor, no en el nombre de la variable.

x = 10
x = "ahora soy texto"

Esto es válido. Pero que sea válido no significa que siempre sea buena idea.

Tipos básicos

Los tipos básicos que debes conocer hoy son:

int: números enteros float: números con decimales str: texto bool: valores booleanos (True y False)

Ejemplos:

age = 28 # int
price = 19.99 # float
name = "Luis"# str
is_active = True # bool

Python distingue mayúsculas y minúsculas

Python diferencia entre name, Name y NAME. Son variables distintas.
