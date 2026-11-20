Un str es una secuencia de caracteres. Eso significa que puedes acceder a sus posiciones individuales.

Índices

Los índices comienzan en 0.

text = "Python"
print(text[0])

Resultado: P

También puedes usar índices negativos.

print(text[- 1])

Resultado: n

Slicing

Permite obtener una parte del string.

text = "Python"
print(text[0:2])
print(text[2:])
print(text[:4])

Inmutabilidad

Los strings en Python son inmutables. Eso significa que no puedes modificar un carácter individual directamente.

Métodos comunes

lower()
upper()
strip()
replace()
split()
join()
startswith()
endswith()
find()
