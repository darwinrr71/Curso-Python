Cuando un programa crece, tener todo en un solo archivo se vuelve confuso. Los módulos permiten separar responsabilidades. Un módulo es, en términos simples, un archivo `.py`.

Import básico

```python
import math

print(math.sqrt(16))
```

Import específico

```python
from math import sqrt

print(sqrt(16))
```

Import con alias

```python
import math as m

print(m.pi)
```
