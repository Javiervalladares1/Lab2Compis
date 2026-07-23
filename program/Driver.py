import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from SimpleLangLexer import SimpleLangLexer
from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor


class CountingErrorListener(ErrorListener):
    """Cuenta errores léxicos y sintácticos sin duplicar su salida en consola."""

    def __init__(self):
        super().__init__()
        self.count = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.count += 1


class TypeCheckVisitor(SimpleLangVisitor):
    """Comprobador de tipos implementado con el patrón Visitor.

    Cada método visit* devuelve el tipo de la expresión visitada:
    'int', 'float', 'bool' o 'error' si el tipo no pudo determinarse.
    Los tipos de las variables se guardan en una tabla de símbolos
    (un diccionario nombre -> tipo).
    """

    NUMERIC = ('int', 'float')

    def __init__(self):
        self.symbols = {}   # tabla de símbolos: nombre de variable -> tipo
        self.errors = []    # lista de errores de tipo encontrados

    def report(self, ctx, message):
        self.errors.append(f"linea {ctx.start.line}: {message}")

    # ---- instrucciones ----

    def visitAssign(self, ctx):
        name = ctx.ID().getText()
        expr_type = self.visit(ctx.expr())
        if expr_type == 'error':
            return None
        # CONFLICTO: reasignar una variable con un tipo distinto al que ya tiene
        if name in self.symbols and self.symbols[name] != expr_type:
            self.report(ctx, f"no se puede asignar '{expr_type}' a la variable "
                             f"'{name}' que ya es de tipo '{self.symbols[name]}'")
            return None
        self.symbols[name] = expr_type
        return None

    def visitPrintExpr(self, ctx):
        self.visit(ctx.expr())
        return None

    def visitBlank(self, ctx):
        return None

    # ---- expresiones ----

    def visitMulDiv(self, ctx):
        return self.arithmetic(ctx)

    def visitAddSub(self, ctx):
        return self.arithmetic(ctx)

    def arithmetic(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text
        if left == 'error' or right == 'error':
            return 'error'
        # CONFLICTO: operación aritmética con un booleano
        if left == 'bool' or right == 'bool':
            self.report(ctx, f"operacion aritmetica '{op}' no valida con tipo 'bool' "
                             f"({left} {op} {right})")
            return 'error'
        # CONFLICTO original del laboratorio: mezclar int con float
        if left != right:
            self.report(ctx, f"no se puede operar '{left}' {op} '{right}': "
                             f"los tipos deben coincidir")
            return 'error'
        return left

    def visitComparison(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text
        if left == 'error' or right == 'error':
            return 'error'
        # CONFLICTO: comparar tipos incompatibles (solo numericos y del mismo tipo)
        if left not in self.NUMERIC or right not in self.NUMERIC or left != right:
            self.report(ctx, f"comparacion '{op}' entre tipos incompatibles "
                             f"({left} {op} {right})")
            return 'error'
        return 'bool'

    def visitEquality(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text
        if left == 'error' or right == 'error':
            return 'error'
        # CONFLICTO: igualdad entre tipos distintos
        if left != right:
            self.report(ctx, f"igualdad '{op}' entre tipos incompatibles "
                             f"({left} {op} {right})")
            return 'error'
        return 'bool'

    def visitInt(self, ctx):
        return 'int'

    def visitFloat(self, ctx):
        return 'float'

    def visitBool(self, ctx):
        return 'bool'

    def visitId(self, ctx):
        name = ctx.ID().getText()
        # CONFLICTO: usar una variable que nunca fue declarada/asignada
        if name not in self.symbols:
            self.report(ctx, f"la variable '{name}' no ha sido declarada")
            return 'error'
        return self.symbols[name]

    def visitParens(self, ctx):
        return self.visit(ctx.expr())


def main(argv):
    # 1. Se lee el archivo de entrada
    input_stream = FileStream(argv[1])

    # 2. Analisis lexico y sintactico
    syntax_errors = CountingErrorListener()
    lexer = SimpleLangLexer(input_stream)
    lexer.addErrorListener(syntax_errors)
    stream = CommonTokenStream(lexer)
    parser = SimpleLangParser(stream)
    parser.addErrorListener(syntax_errors)
    tree = parser.prog()

    # Si hay errores lexicos o sintacticos, ANTLR ya los imprimio en consola
    if syntax_errors.count > 0:
        print(">> El programa tiene errores lexicos o sintacticos: "
              "no se ejecuta el chequeo de tipos.")
        sys.exit(1)

    # 3. Analisis semantico: chequeo de tipos con Visitor
    checker = TypeCheckVisitor()
    checker.visit(tree)

    if checker.errors:
        print(">> Errores de tipo encontrados (Visitor):")
        for error in checker.errors:
            print("   " + error)
        sys.exit(1)

    print(">> La validacion de tipos fue exitosa (Visitor).")


if __name__ == '__main__':
    main(sys.argv)
