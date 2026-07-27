import sys
from antlr4 import *
from SimpleLangLexer import SimpleLangLexer
from SimpleLangParser import SimpleLangParser
from SimpleLangListener import SimpleLangListener


class TypeCheckListener(SimpleLangListener):
    """Comprobador de tipos implementado con el patrón Listener.

    A diferencia del Visitor, el Listener no controla el recorrido ni
    devuelve valores: ANTLR recorre el árbol automáticamente y dispara
    los métodos exit* al salir de cada nodo. Como los hijos se procesan
    antes que el padre, al salir de un nodo ya conocemos los tipos de
    sus subexpresiones; se anotan en el diccionario self.types
    (nodo del árbol -> tipo).
    """

    NUMERIC = ('int', 'float')

    def __init__(self):
        self.symbols = {}   # tabla de símbolos: nombre de variable -> tipo
        self.types = {}     # tipo calculado para cada nodo de expresión
        self.errors = []    # lista de errores de tipo encontrados

    def report(self, ctx, message):
        self.errors.append(f"linea {ctx.start.line}: {message}")

    # ---- instrucciones ----

    def exitAssign(self, ctx):
        name = ctx.ID().getText()
        expr_type = self.types[ctx.expr()]
        if expr_type == 'error':
            return
        # CONFLICTO: reasignar una variable con un tipo distinto al que ya tiene
        if name in self.symbols and self.symbols[name] != expr_type:
            self.report(ctx, f"no se puede asignar '{expr_type}' a la variable "
                             f"'{name}' que ya es de tipo '{self.symbols[name]}'")
            return
        self.symbols[name] = expr_type

    # ---- expresiones ----

    def exitMulDiv(self, ctx):
        self.arithmetic(ctx)

    def exitAddSub(self, ctx):
        self.arithmetic(ctx)

    def arithmetic(self, ctx):
        left = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op = ctx.op.text
        if left == 'error' or right == 'error':
            self.types[ctx] = 'error'
            return
        # CONFLICTO: operación aritmética con un booleano
        if left == 'bool' or right == 'bool':
            self.report(ctx, f"operacion aritmetica '{op}' no valida con tipo 'bool' "
                             f"({left} {op} {right})")
            self.types[ctx] = 'error'
            return
        # CONFLICTO original del laboratorio: mezclar int con float
        if left != right:
            self.report(ctx, f"no se puede operar '{left}' {op} '{right}': "
                             f"los tipos deben coincidir")
            self.types[ctx] = 'error'
            return
        self.types[ctx] = left

    def exitComparison(self, ctx):
        left = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op = ctx.op.text
        if left == 'error' or right == 'error':
            self.types[ctx] = 'error'
            return
        # CONFLICTO: comparar tipos incompatibles (solo numericos y del mismo tipo)
        if left not in self.NUMERIC or right not in self.NUMERIC or left != right:
            self.report(ctx, f"comparacion '{op}' entre tipos incompatibles "
                             f"({left} {op} {right})")
            self.types[ctx] = 'error'
            return
        self.types[ctx] = 'bool'

    def exitEquality(self, ctx):
        left = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op = ctx.op.text
        if left == 'error' or right == 'error':
            self.types[ctx] = 'error'
            return
        # CONFLICTO: igualdad entre tipos distintos
        if left != right:
            self.report(ctx, f"igualdad '{op}' entre tipos incompatibles "
                             f"({left} {op} {right})")
            self.types[ctx] = 'error'
            return
        self.types[ctx] = 'bool'

    def exitInt(self, ctx):
        self.types[ctx] = 'int'

    def exitFloat(self, ctx):
        self.types[ctx] = 'float'

    def exitBool(self, ctx):
        self.types[ctx] = 'bool'

    def exitId(self, ctx):
        name = ctx.ID().getText()
        # CONFLICTO: usar una variable que nunca fue declarada/asignada
        if name not in self.symbols:
            self.report(ctx, f"la variable '{name}' no ha sido declarada")
            self.types[ctx] = 'error'
            return
        self.types[ctx] = self.symbols[name]

    def exitParens(self, ctx):
        self.types[ctx] = self.types[ctx.expr()]


def main(argv):
    # 1. Se lee el archivo de entrada
    input_stream = FileStream(argv[1])

    # 2. Analisis lexico y sintactico
    lexer = SimpleLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SimpleLangParser(stream)
    tree = parser.prog()

    # Si hay errores sintacticos, ANTLR ya los imprimio en consola
    if parser.getNumberOfSyntaxErrors() > 0:
        print(">> El programa tiene errores sintacticos: no se ejecuta el chequeo de tipos.")
        sys.exit(1)

    # 3. Analisis semantico: chequeo de tipos con Listener.
    #    ParseTreeWalker recorre el arbol automaticamente y dispara los exit*.
    checker = TypeCheckListener()
    walker = ParseTreeWalker()
    walker.walk(checker, tree)

    if checker.errors:
        print(">> Errores de tipo encontrados (Listener):")
        for error in checker.errors:
            print("   " + error)
        sys.exit(1)

    print(">> La validacion de tipos fue exitosa (Listener).")


if __name__ == '__main__':
    main(sys.argv)
