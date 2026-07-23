# Laboratorio 2: Sistema de Tipos con ANTLR

## Descripción general

ANTLR (*ANother Tool for Language Recognition*) es un generador de analizadores: a partir de una gramática `.g4` produce automáticamente el **lexer** (convierte texto en tokens) y el **parser** (verifica la estructura sintáctica y construye el árbol de análisis). Además, ANTLR genera dos mecanismos para recorrer ese árbol: el **Visitor** y el **Listener**.

En este laboratorio se trabaja con un lenguaje pequeño llamado **SimpleLang** (asignaciones y expresiones) y se agrega una etapa nueva que no existía en el Laboratorio 1: el **análisis semántico**, implementado como un **sistema de tipos básico**. Ya no basta con que el programa esté bien escrito sintácticamente: ahora también se verifica que las operaciones tengan sentido según los tipos de sus operandos (`int`, `float`, `bool`). Por ejemplo, `5 + true` es sintácticamente válido, pero el sistema de tipos lo rechaza porque no se puede sumar un entero con un booleano.

El chequeo de tipos se implementó **dos veces**, con los dos enfoques que ofrece ANTLR: una versión con **Visitor** (`Driver.py`) y una con **Listener** (`DriverListener.py`), que producen exactamente los mismos diagnósticos.

Se usa **Python** para las pruebas porque el runtime de ANTLR para Python permite escribir los comprobadores en muy pocas líneas, fáciles de leer y de modificar. Todo el entorno (Java, ANTLR y el runtime de Python) está encapsulado en **Docker**, así que no hay que instalar nada localmente.

## Relación con el contenido del curso

El material del curso (basado en *Compiladores: principios, técnicas y herramientas* de Aho, Lam, Sethi y Ullman, capítulos 5–8) cubre exactamente la etapa que este laboratorio implementa:

- **Análisis semántico**: el curso presenta el pipeline *stream de tokens → parser → comprobador de tipos → árbol sintáctico → generador de código intermedio*. La comprobación de tipos aparece como la principal revisión semántica, cuyo objetivo es **prevenir errores en tiempo de ejecución**: verificar que el tipo de una construcción coincida con el tipo esperado en su contexto. Este laboratorio implementa precisamente ese "comprobador de tipos" que se inserta después del parser.
- **Sistema de tipos**: el curso lo define como una **colección de reglas de inferencia** que asignan expresiones de tipo a las distintas partes de un programa, con juicios de la forma Γ ⊢ M : T ("M tiene tipo T en el ambiente Γ"). En el material se muestra el sistema de tipos de Decaf con reglas como: si M : int y N : int entonces (M + N) : int; y las comparaciones (M < N, M >= N) producen boolean. Las reglas que implementamos en este laboratorio son una versión reducida de esas mismas reglas: la aritmética exige operandos numéricos del mismo tipo, y las comparaciones e igualdades devuelven `bool`.
- **Traducción dirigida por la sintaxis** (capítulo 5): el curso explica que a cada producción de la gramática se le asocian reglas semánticas que calculan **atributos sintetizados**, evaluados de abajo hacia arriba en el árbol (recorrido postorder). El tipo de cada expresión en este laboratorio es exactamente un atributo sintetizado: el tipo de `x + y` se calcula a partir de los tipos de `x` y de `y`. El Visitor y el Listener son las dos formas concretas que da ANTLR de hacer ese recorrido y evaluar las reglas.
- **Tabla de símbolos**: el curso la define como la estructura que **enlaza nombres con objetos** y su información (nombre, tipo de dato, etc.), con operaciones como *insert* y *lookup*, y responde preguntas como "¿el símbolo fue declarado antes de usarse?". Nuestra tabla de símbolos es un diccionario `nombre → tipo` que hace exactamente eso: se inserta el tipo al asignar una variable y se consulta al usarla (detectando variables no declaradas).
- El material también menciona el uso de un **AST visitor** para recolectar información de símbolos (el *Symbol Generator*), y que el proyecto del curso es un compilador de **Decaf** construido con **ANTLR** — este laboratorio es práctica directa de esas herramientas a pequeña escala.

## Estructura del proyecto

```
Laboratorio2/
├── Dockerfile                          # Imagen con Java, ANTLR 4.13.2 y Python
├── README.md                           # Este documento
└── program/
    ├── SimpleLang.g4                   # Gramática del lenguaje SimpleLang
    ├── Driver.py                       # Chequeo de tipos con VISITOR
    ├── DriverListener.py               # Chequeo de tipos con LISTENER
    ├── program_test_pass.txt           # Prueba que debe pasar
    ├── program_test_no_pass.txt        # Prueba con 5 errores de tipo
    ├── program_test_extra_pass.txt     # Prueba extra de las operaciones nuevas
    ├── program_test_extra_no_pass.txt  # Prueba extra con errores sintácticos
    └── (archivos generados por ANTLR, ver abajo)
```

- **`Dockerfile`**: imagen basada en Python 3.11 con Java (necesario para ejecutar la herramienta ANTLR), el JAR de ANTLR 4.13.2, el runtime `antlr4-python3-runtime` de la misma versión, y el comando `antlr` listo para usar. El directorio de trabajo es `/program`.
- **`SimpleLang.g4`**: la gramática, con las reglas del parser (`prog`, `stat`, `expr`) y los tokens. Incluye las dos operaciones nuevas (comparación e igualdad).
- **`Driver.py`**: contiene la clase `TypeCheckVisitor` (hereda de `SimpleLangVisitor`) y el `main` que ejecuta el análisis con el enfoque **Visitor**.
- **`DriverListener.py`**: contiene la clase `TypeCheckListener` (hereda de `SimpleLangListener`) y el `main` que ejecuta el análisis con el enfoque **Listener**.
- **Archivos generados por ANTLR** (aparecen en `program/` tras ejecutar la herramienta; no se editan a mano):
  - `SimpleLangLexer.py` — el analizador léxico.
  - `SimpleLangParser.py` — el analizador sintáctico.
  - `SimpleLangVisitor.py` — clase base del Visitor: un método `visitX` por cada alternativa etiquetada de la gramática (se genera con la opción `-visitor`).
  - `SimpleLangListener.py` — clase base del Listener: métodos `enterX`/`exitX` por cada alternativa (se genera por defecto o con `-listener`).
  - `SimpleLang.tokens`, `SimpleLangLexer.tokens`, `SimpleLang.interp`, `SimpleLangLexer.interp` — tablas y datos internos de ANTLR.

## Configuración del entorno

Desde la carpeta `Laboratorio2/` (donde está el `Dockerfile`):

```bash
docker build --rm . -t lab2-image && docker run --rm -ti -v "$(pwd)/program":/program lab2-image
```

- `docker build --rm . -t lab2-image` construye la imagen y la etiqueta como `lab2-image`.
- `docker run --rm -ti ... lab2-image` abre una terminal interactiva dentro del contenedor (`-ti`); con `--rm` el contenedor se elimina al salir.

**¿Qué significa el volumen `-v "$(pwd)/program":/program`?**

Monta la carpeta `program/` de tu computadora dentro del contenedor en la ruta `/program`. La carpeta queda **compartida**: los archivos que ANTLR genere dentro del contenedor aparecen también en tu máquina, y cualquier edición que hagas afuera (por ejemplo, cambiar la gramática) se ve de inmediato adentro. `$(pwd)` se expande a la ruta del directorio actual, por eso el comando debe correrse desde `Laboratorio2/`.

## Generación del Lexer y Parser

Dentro del contenedor (ya estás en `/program`):

```bash
# Genera lexer, parser y el Visitor (SimpleLangVisitor.py)
antlr -Dlanguage=Python3 -visitor SimpleLang.g4

# Genera lexer, parser y el Listener (SimpleLangListener.py)
antlr -Dlanguage=Python3 -listener SimpleLang.g4
```

- `-Dlanguage=Python3` indica que el código generado sea Python 3 (por defecto sería Java).
- `-visitor` agrega la generación de `SimpleLangVisitor.py`, la clase base para el patrón Visitor. Además, el parser se genera con los métodos `accept()` que permiten el *dispatch* del Visitor.
- `-listener` genera `SimpleLangListener.py`, la clase base para el patrón Listener (en realidad el Listener se genera **por defecto**, así que esta bandera solo lo hace explícito).

> **Importante — orden de los comandos:** cada ejecución de `antlr` **sobrescribe** `SimpleLangParser.py`. Si el último comando que corres es solo `-listener`, el parser se regenera **sin** el soporte del Visitor y `Driver.py` dejará de detectar errores (el Visitor recorre el árbol de forma genérica sin entrar a tus métodos). Por eso, la forma recomendada es generar todo de una sola vez:
>
> ```bash
> antlr -Dlanguage=Python3 -visitor -listener SimpleLang.g4
> ```
>
> Este único comando genera el lexer, el parser, el Visitor y el Listener, todos consistentes entre sí. (Si prefieres correr los dos comandos por separado, corre `-listener` primero y `-visitor` de último.)

## Ejecución del analizador

**Con Visitor:**

```bash
python3 Driver.py program_test_pass.txt
python3 Driver.py program_test_no_pass.txt
```

**Con Listener:**

```bash
python3 DriverListener.py program_test_pass.txt
python3 DriverListener.py program_test_no_pass.txt
```

- Si el archivo **pasa** (sintaxis correcta y sin conflictos de tipos), se imprime:
  `>> La validacion de tipos fue exitosa (Visitor).` (o `(Listener)` según el driver).
- Si el archivo tiene **errores de tipo**, se listan todos con su número de línea y el programa termina con código de salida 1.
- Si el archivo tiene **errores léxicos o sintácticos**, ANTLR los imprime en consola (línea, columna y descripción) y el chequeo de tipos no se ejecuta.

## Explicación de la gramática SimpleLang.g4

### Regla inicial: `prog`

```antlr
prog: stat+ EOF ;
```

Un programa es **una o más instrucciones** (`stat`) y debe consumir toda la entrada (`EOF`). Es la regla desde la que ambos drivers inician el análisis (`parser.prog()`).

### Instrucciones: `stat`

```antlr
stat: expr NEWLINE          # printExpr
    | ID '=' expr NEWLINE   # assign
    | NEWLINE               # blank
    ;
```

El lenguaje acepta tres tipos de instrucción: una **expresión sola** (`x + 1`), una **asignación** (`x = 5`) — que es la forma en que se "declaran" las variables: una variable queda declarada con el tipo de la primera expresión que se le asigna — y una **línea en blanco**. Toda instrucción termina con salto de línea. Los `# nombres` no son comentarios: son **etiquetas de alternativa** de ANTLR; gracias a ellas el Visitor y el Listener generados tienen un método por cada caso (`visitAssign`, `exitMulDiv`, etc.), que es lo que hace posible el chequeo de tipos por regla.

### Expresiones: `expr`

```antlr
expr: expr op=(MUL|DIV) expr    # MulDiv
    | expr op=(ADD|SUB) expr    # AddSub
    | expr op=(LT|GT) expr      # Comparison   <- NUEVA
    | expr op=(EQ|NEQ) expr     # Equality     <- NUEVA
    | INT                       # int
    | FLOAT                     # float
    | BOOL                      # bool
    | ID                        # id
    | '(' expr ')'              # parens
    ;
```

- **Operaciones originales**: multiplicación/división (`MulDiv`) y suma/resta (`AddSub`).
- **Operaciones nuevas agregadas**: comparación relacional `<` `>` (`Comparison`) e igualdad/desigualdad `==` `!=` (`Equality`). Ver la sección "Operaciones agregadas".
- La regla es recursiva y el **orden de las alternativas define la precedencia**: `*` y `/` atan más fuerte que `+` y `-`, que atan más fuerte que `<` y `>`, y la igualdad es la de menor precedencia. Así, `x + y * 2 < z == true` se agrupa como `((x + (y*2)) < z) == true`.
- `op=` le da un nombre al token del operador, para poder consultarlo desde Python (`ctx.op.text`).

### Tokens (reglas del lexer)

```antlr
MUL: '*' ;  DIV: '/' ;  ADD: '+' ;  SUB: '-' ;
LT: '<' ;   GT: '>' ;   EQ: '==' ;  NEQ: '!=' ;
BOOL    : 'true' | 'false' ;
ID      : [a-zA-Z]+ ;
INT     : [0-9]+ ;
FLOAT   : [0-9]+ '.' [0-9]+ ;
NEWLINE : '\r'? '\n' ;
WS      : [ \t]+ -> skip ;
```

- **Identificadores (`ID`)**: una o más letras (`x`, `edad`, `esGrande`). Sin dígitos ni guiones bajos: el lenguaje es deliberadamente simple.
- **Números**: `INT` es uno o más dígitos (`5`, `42`); `FLOAT` exige dígitos, punto y dígitos (`2.5`, `3.14`). El lexer siempre elige la coincidencia más larga, por eso `2.5` es un solo token `FLOAT` y no `INT . INT`.
- **Booleanos (`BOOL`)**: los literales `true` y `false`. La regla está **antes que `ID`** a propósito: cuando dos reglas del lexer empatan en longitud, gana la primera; sin ese orden, `true` sería un identificador.
- **`NEWLINE`**: el salto de línea **no se ignora** porque marca el final de cada instrucción.
- **`WS` con `-> skip`**: espacios y tabulaciones se reconocen pero se descartan; nunca llegan al parser. Por eso `x=5` y `x  =  5` son equivalentes.
- Un carácter fuera de todo token (por ejemplo `@`) produce un error léxico: `token recognition error at: '@'`.

## Sistema de tipos

- **Tipos del lenguaje**: `int` (enteros), `float` (flotantes) y `bool` (booleanos). Internamente existe además el pseudo-tipo `error`, que marca una expresión cuyo tipo no pudo determinarse y evita reportar errores en cascada.
- **Tabla de símbolos**: un diccionario `self.symbols` de `nombre → tipo`. Al ejecutar una asignación se hace *insert* (la variable queda declarada con el tipo de la expresión); al usar una variable en una expresión se hace *lookup*.
- **Validación de una asignación** (`ID = expr`): primero se calcula el tipo de la expresión derecha. Si la variable no existía, se registra con ese tipo. Si ya existía **con otro tipo**, se reporta un conflicto (no hay conversión implícita en SimpleLang).
- **Validación de una operación**: cada operador tiene su regla de inferencia, igual que en el material del curso:
  - Aritmética (`+ - * /`): ambos operandos deben ser numéricos (`int` o `float`) **y del mismo tipo**; el resultado tiene ese mismo tipo. (Γ ⊢ M : int, Γ ⊢ N : int ⟹ Γ ⊢ M+N : int)
  - Comparación (`< >`): ambos operandos numéricos y del mismo tipo; el resultado es `bool`. (Γ ⊢ M : int, Γ ⊢ N : int ⟹ Γ ⊢ M<N : bool)
  - Igualdad (`== !=`): ambos operandos del **mismo tipo** (incluye `bool == bool`); el resultado es `bool`.
- **Detección de conflictos**: si una regla no se cumple, se agrega un mensaje con el número de línea a la lista `self.errors` y la expresión recibe tipo `error`. El tipo `error` se propaga hacia arriba sin generar mensajes adicionales (si `t` no está declarada, `t + 1` no reporta además un error de suma).
- **Al terminar el recorrido**: si hay errores acumulados se imprimen todos y el programa sale con código 1; si no, se imprime el mensaje de validación exitosa.

## Visitor

- **Archivo**: `Driver.py`, clase `TypeCheckVisitor`, que hereda de la clase generada `SimpleLangVisitor` (de `SimpleLangVisitor.py`).
- **Métodos importantes**: un `visitX` por cada alternativa etiquetada de la gramática: `visitAssign`, `visitMulDiv`, `visitAddSub`, `visitComparison`, `visitEquality`, `visitInt`, `visitFloat`, `visitBool`, `visitId`, `visitParens`.
- **Cómo visita los nodos**: el recorrido lo controla el propio código. `checker.visit(tree)` arranca en la raíz y cada método decide explícitamente qué hijos visitar llamando `self.visit(ctx.expr(0))`, `self.visit(ctx.expr(1))`, etc.
- **Cómo calcula los tipos**: cada método **devuelve** el tipo de su subexpresión como valor de retorno. Por ejemplo, `visitAddSub` visita el operando izquierdo y el derecho, recibe sus tipos como retorno, aplica la regla de inferencia y devuelve el tipo resultante. Es la forma más directa de implementar atributos sintetizados.
- **Cómo reporta errores**: el método `report(ctx, mensaje)` agrega `linea N: mensaje` a la lista de errores usando `ctx.start.line`; al final `main` los imprime todos.

## Listener

- **Archivo**: `DriverListener.py`, clase `TypeCheckListener`, que hereda de la clase generada `SimpleLangListener` (de `SimpleLangListener.py`).
- **Cómo se recorre el árbol**: no lo recorre nuestro código, sino ANTLR: `ParseTreeWalker().walk(checker, tree)` camina el árbol completo en profundidad y dispara automáticamente los eventos `enterX` al entrar a un nodo y `exitX` al salir. Nosotros solo implementamos los `exitX` que nos interesan.
- **Diferencia clave con el Visitor**: los métodos del Listener **no pueden devolver valores**. Para pasar el tipo de una subexpresión a su padre se usa un diccionario auxiliar `self.types` que asocia cada nodo del árbol con su tipo (`self.types[ctx] = 'int'`). Como el walker sale de los hijos antes que del padre, cuando se ejecuta `exitAddSub` los tipos de `ctx.expr(0)` y `ctx.expr(1)` ya están anotados en el diccionario.
- **Cómo se validan los tipos**: las reglas son exactamente las mismas que en el Visitor (misma aritmética, comparación, igualdad, asignación y tabla de símbolos); solo cambia la mecánica: en lugar de retornar el tipo, se escribe en `self.types[ctx]`.
- **Cómo reporta errores**: igual que el Visitor — lista `self.errors` con línea y mensaje, impresa al final. Ambos drivers producen la misma salida para la misma entrada.

## Diferencia entre Visitor y Listener

- **Visitor**: el programador controla manualmente qué nodos visitar y cada método puede **devolver un valor** (aquí, el tipo). Puede incluso podar ramas que no le interesen. Ideal cuando el resultado de un nodo depende del resultado de sus hijos, como en un chequeo de tipos o un intérprete.
- **Listener**: ANTLR recorre el árbol **automáticamente** y avisa con eventos de entrada (`enterX`) y salida (`exitX`). No devuelve valores, así que la información se comunica con estructuras auxiliares. Ideal cuando se quiere reaccionar a construcciones sin administrar el recorrido.
- **En este laboratorio ambos se usan para lo mismo**: validar las reglas semánticas y los conflictos de tipos de SimpleLang, demostrando que el mismo análisis puede implementarse con los dos enfoques y produce resultados idénticos.

## Operaciones agregadas

Las operaciones originales del lenguaje eran la aritmética (`* / + -`). Se agregaron **dos operaciones nuevas**:

### 1. Comparación relacional: `<` y `>`

- **Sintaxis**: `expr < expr` o `expr > expr` (alternativa `# Comparison` de la gramática).
- **Ejemplo válido**:
  ```
  edad = 20
  limite = 18
  mayor = edad > limite
  ```
- **Tipos que acepta**: ambos operandos numéricos (`int` con `int`, o `float` con `float`). El resultado es `bool`.
- **Errores que puede generar**: comparar tipos distintos (`x < 2.5` con `x` entero) o comparar booleanos (`true < false`) produce `comparacion '<' entre tipos incompatibles`.

### 2. Igualdad y desigualdad: `==` y `!=`

- **Sintaxis**: `expr == expr` o `expr != expr` (alternativa `# Equality` de la gramática).
- **Ejemplo válido**:
  ```
  iguales = edad == limite
  listo = activo == mayor
  ```
- **Tipos que acepta**: ambos operandos del **mismo tipo**: `int == int`, `float == float` o `bool == bool`. El resultado es `bool`.
- **Errores que puede generar**: igualar tipos distintos (`true == 5`, `2.5 != 2`) produce `igualdad '==' entre tipos incompatibles`.

Estas operaciones son las que introducen valores `bool` "calculados" al lenguaje, lo que a su vez hace posibles varios de los conflictos de tipos nuevos.

## Conflictos de tipos agregados

El conflicto **original** del laboratorio es mezclar `int` con `float` en la aritmética (`z = x + y` con `x` entero y `y` flotante). Sobre esa base se agregaron **cuatro conflictos adicionales** (el requisito pedía al menos tres):

### 1. Operación aritmética con un booleano

- **Descripción**: `+ - * /` solo aceptan operandos numéricos; usar un `bool` es un error.
- **Código incorrecto**: `w = x + true` (con `x` entero).
- **Mensaje esperado**: `linea 4: operacion aritmetica '+' no valida con tipo 'bool' (int + bool)`

### 2. Asignar a una variable un tipo distinto al que ya tiene

- **Descripción**: una variable queda declarada con el tipo de su primera asignación; reasignarla con otro tipo es un conflicto (equivale a "asignar un booleano a una variable entera").
- **Código incorrecto**: `x = 5` seguido de `x = false`.
- **Mensaje esperado**: `linea 5: no se puede asignar 'bool' a la variable 'x' que ya es de tipo 'int'`

### 3. Comparar tipos incompatibles

- **Descripción**: `<`, `>`, `==`, `!=` exigen operandos compatibles (numéricos del mismo tipo para `<` `>`; mismo tipo para `==` `!=`).
- **Código incorrecto**: `b = x < 2.5` (con `x` entero).
- **Mensaje esperado**: `linea 7: comparacion '<' entre tipos incompatibles (int < float)`

### 4. Usar una variable no declarada

- **Descripción**: usar en una expresión una variable a la que nunca se le asignó valor; la tabla de símbolos no la encuentra (*lookup* falla).
- **Código incorrecto**: `v = t + 1` (la variable `t` no existe).
- **Mensaje esperado**: `linea 6: la variable 't' no ha sido declarada`

## Pruebas

Todos los comandos se ejecutan dentro del contenedor, después de generar los archivos con:

```bash
antlr -Dlanguage=Python3 -visitor -listener SimpleLang.g4
```

**1. Prueba que pasa con Visitor:**

```bash
python3 Driver.py program_test_pass.txt
# >> La validacion de tipos fue exitosa (Visitor).
```

**2. Prueba que no pasa con Visitor** (contiene el conflicto original y los cuatro nuevos):

```bash
python3 Driver.py program_test_no_pass.txt
# >> Errores de tipo encontrados (Visitor):
#    linea 3: no se puede operar 'int' + 'float': los tipos deben coincidir
#    linea 4: operacion aritmetica '+' no valida con tipo 'bool' (int + bool)
#    linea 5: no se puede asignar 'bool' a la variable 'x' que ya es de tipo 'int'
#    linea 6: la variable 't' no ha sido declarada
#    linea 7: comparacion '<' entre tipos incompatibles (int < float)
```

**3. Prueba que pasa con Listener:**

```bash
python3 DriverListener.py program_test_pass.txt
# >> La validacion de tipos fue exitosa (Listener).
```

**4. Prueba que no pasa con Listener** (los mismos cinco errores que con Visitor):

```bash
python3 DriverListener.py program_test_no_pass.txt
```

**5. Pruebas de las dos operaciones nuevas** (`program_test_extra_pass.txt` usa `<`, `>`, `==` y `!=` con `int`, `float` y `bool`):

```bash
python3 Driver.py program_test_extra_pass.txt
python3 DriverListener.py program_test_extra_pass.txt
# ambas: validacion exitosa
```

**6. Pruebas de los conflictos de tipos nuevos**: están todos dentro de `program_test_no_pass.txt` (comandos 2 y 4). Además, `program_test_extra_no_pass.txt` contiene **errores sintácticos** para ver la otra categoría de fallo:

```bash
python3 Driver.py program_test_extra_no_pass.txt
# line 1:7 extraneous input '\n' expecting {'(', BOOL, ID, INT, FLOAT}
# line 2:2 mismatched input '=' expecting NEWLINE
# line 3:1 missing NEWLINE at 'z'
# line 4:2 token recognition error at: '@'
# line 4:4 no viable alternative at input 'w4'
# >> El programa tiene errores lexicos o sintacticos: no se ejecuta el chequeo de tipos.
```

## Resultado esperado

- Si el programa es **léxica y sintácticamente correcto y no tiene errores de tipo**, aparece el mensaje de validación exitosa (`>> La validacion de tipos fue exitosa ...`).
- Si el programa tiene **errores léxicos o sintácticos**, ANTLR los muestra en consola con línea y columna, y el chequeo de tipos no se ejecuta.
- Si el programa tiene **errores de tipo**, el sistema de tipos los muestra en consola con su número de línea (todos, no solo el primero).
- `program_test_pass.txt` y `program_test_extra_pass.txt` **pasan** con ambos drivers.
- `program_test_no_pass.txt` **no pasa** (5 errores de tipo) y `program_test_extra_no_pass.txt` **no pasa** (errores sintácticos), con ambos drivers.

## Guion breve para video

> Hola, en este video les muestro mi Laboratorio 2 del curso de Construcción de Compiladores: un sistema de tipos hecho con ANTLR.
>
> En el laboratorio pasado ANTLR solo revisaba la sintaxis. Ahora agregamos la siguiente etapa que vimos en el curso: el análisis semántico. La idea es la que vimos en clase con las reglas de inferencia: por ejemplo, si M es int y N es int, entonces M más N es int. Si eso no se cumple, es un conflicto de tipos y el compilador lo tiene que reportar.
>
> El lenguaje se llama SimpleLang: tiene asignaciones y expresiones, con tres tipos: int, float y bool. Todo corre en Docker, así que primero construyo la imagen y abro el contenedor con este comando... [correr `docker build --rm . -t lab2-image && docker run --rm -ti -v "$(pwd)/program":/program lab2-image`]. La carpeta program queda montada como volumen, así que lo que se genera adentro también queda en mi máquina.
>
> Ya adentro, genero el lexer, el parser, el visitor y el listener con un solo comando: `antlr -Dlanguage=Python3 -visitor -listener SimpleLang.g4`. La bandera visitor genera la clase base del Visitor y la bandera listener la del Listener. Si listan los archivos, ahí están SimpleLangLexer, SimpleLangParser, SimpleLangVisitor y SimpleLangListener.
>
> Rapidito sobre la gramática: la regla inicial es prog, que es una lista de instrucciones. Una instrucción es una expresión o una asignación. Las expresiones ya traían suma, resta, multiplicación y división, y yo le agregué dos operaciones nuevas: la comparación, con menor que y mayor que, y la igualdad, con igual-igual y distinto. Las dos devuelven tipo bool. Abajo están los tokens: los números enteros y flotantes, los literales true y false, y el skip que ignora los espacios.
>
> El chequeo de tipos está implementado dos veces, porque el lab pide usar ambos enfoques. Driver.py usa el Visitor: cada método visita sus operandos, recibe los tipos como valor de retorno, aplica la regla y devuelve el tipo del resultado. DriverListener.py usa el Listener: ahí ANTLR recorre el árbol solo, y a mí solo me avisa cuando sale de cada nodo; como el Listener no puede devolver valores, los tipos se van anotando en un diccionario. Esa es justo la diferencia entre los dos patrones: con Visitor yo controlo el recorrido y retorno valores; con Listener el recorrido es automático y por eventos. Los dos usan la misma tabla de símbolos, que guarda el tipo de cada variable, como vimos en el curso.
>
> Probemos el archivo que sí pasa: `python3 Driver.py program_test_pass.txt`... y dice que la validación de tipos fue exitosa. Con el Listener: `python3 DriverListener.py program_test_pass.txt`... lo mismo.
>
> Ahora el que no pasa: `python3 Driver.py program_test_no_pass.txt`. Miren: reporta cinco errores, cada uno con su línea. Está el clásico de mezclar int con float, y los cuatro conflictos que agregué: sumar un entero con un booleano, asignarle un booleano a una variable que ya era entera, usar una variable que nunca declaré, y comparar un int con un float. Si lo corro con el Listener, salen exactamente los mismos cinco errores.
>
> También tengo un archivo con errores de sintaxis, y ahí es ANTLR quien se queja, con línea y columna, antes de llegar al chequeo de tipos.
>
> Y eso es todo: un mini análisis semántico como el del curso — parser, comprobador de tipos y tabla de símbolos — implementado con Visitor y con Listener sobre ANTLR. Gracias por ver el video.

## Comentario final

En este laboratorio se aprendió a completar la siguiente etapa del pipeline de un compilador: después del análisis léxico y sintáctico con ANTLR (generación del lexer y el parser desde una gramática `.g4`), se implementó el **análisis semántico** mediante un **sistema de tipos básico** con tabla de símbolos, tal como se ve en el material del curso (reglas de inferencia, atributos sintetizados y comprobador de tipos). Se usaron los dos mecanismos de recorrido del árbol que ofrece ANTLR — **Visitor**, con control manual del recorrido y valores de retorno, y **Listener**, con recorrido automático por eventos — comprobando que ambos permiten validar los mismos conflictos de tipos: mezclar `int` con `float`, operar aritméticamente con booleanos, reasignar variables con otro tipo, comparar tipos incompatibles y usar variables no declaradas. Finalmente, **Docker** volvió a garantizar un entorno reproducible con Java, ANTLR y Python, sin problemas de configuración entre máquinas.
