Muchos programas necesitan persistir información. Un archivo es una forma simple de guardar datos en disco.

Modos de apertura

r: lectura w: escritura (sobrescribe) a: añade al final

with open(...)

Maneja el recurso de forma segura. Cierra el archivo automáticamente incluso si ocurre un error.
