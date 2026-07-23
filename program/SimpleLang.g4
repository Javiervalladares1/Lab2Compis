grammar SimpleLang;

// ---------- Reglas del parser ----------

// Regla inicial: un programa es una o más instrucciones y debe consumir toda la entrada
prog: stat+ EOF ;

// Una instrucción puede ser:
//   - una expresión seguida de salto de línea
//   - una asignación (ID = expresión) seguida de salto de línea
//   - una línea en blanco
stat: expr NEWLINE          # printExpr
    | ID '=' expr NEWLINE   # assign
    | NEWLINE               # blank
    ;

// Expresiones. El orden de las alternativas define la precedencia:
// primero * y /, luego + y -, luego las comparaciones y al final la igualdad.
//
// Operaciones originales del laboratorio: MulDiv y AddSub.
// Operaciones NUEVAS agregadas como extensión:
//   - Comparison: comparación relacional  <  >
//   - Equality:   igualdad / desigualdad  ==  !=
expr: expr op=(MUL|DIV) expr    # MulDiv
    | expr op=(ADD|SUB) expr    # AddSub
    | expr op=(LT|GT) expr      # Comparison
    | expr op=(EQ|NEQ) expr     # Equality
    | INT                       # int
    | FLOAT                     # float
    | BOOL                      # bool
    | ID                        # id
    | '(' expr ')'              # parens
    ;

// ---------- Reglas del lexer (tokens) ----------

MUL     : '*' ;
DIV     : '/' ;
ADD     : '+' ;
SUB     : '-' ;
LT      : '<' ;                  // nueva operación: menor que
GT      : '>' ;                  // nueva operación: mayor que
EQ      : '==' ;                 // nueva operación: igualdad
NEQ     : '!=' ;                 // nueva operación: desigualdad
BOOL    : 'true' | 'false' ;     // literales booleanos (antes de ID para tener prioridad)
ID      : [a-zA-Z]+ ;            // identificadores: una o más letras
INT     : [0-9]+ ;               // números enteros: uno o más dígitos
FLOAT   : [0-9]+ '.' [0-9]+ ;    // números flotantes: dígitos . dígitos
NEWLINE : '\r'? '\n' ;           // salto de línea (termina cada instrucción)
WS      : [ \t]+ -> skip ;       // espacios y tabulaciones se ignoran
