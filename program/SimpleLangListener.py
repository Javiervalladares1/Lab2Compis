# Generated from SimpleLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleLangParser import SimpleLangParser
else:
    from SimpleLangParser import SimpleLangParser

# This class defines a complete listener for a parse tree produced by SimpleLangParser.
class SimpleLangListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleLangParser#prog.
    def enterProg(self, ctx:SimpleLangParser.ProgContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#prog.
    def exitProg(self, ctx:SimpleLangParser.ProgContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#printExpr.
    def enterPrintExpr(self, ctx:SimpleLangParser.PrintExprContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#printExpr.
    def exitPrintExpr(self, ctx:SimpleLangParser.PrintExprContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#assign.
    def enterAssign(self, ctx:SimpleLangParser.AssignContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#assign.
    def exitAssign(self, ctx:SimpleLangParser.AssignContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#blank.
    def enterBlank(self, ctx:SimpleLangParser.BlankContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#blank.
    def exitBlank(self, ctx:SimpleLangParser.BlankContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#parens.
    def enterParens(self, ctx:SimpleLangParser.ParensContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#parens.
    def exitParens(self, ctx:SimpleLangParser.ParensContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#bool.
    def enterBool(self, ctx:SimpleLangParser.BoolContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#bool.
    def exitBool(self, ctx:SimpleLangParser.BoolContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#MulDiv.
    def enterMulDiv(self, ctx:SimpleLangParser.MulDivContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#MulDiv.
    def exitMulDiv(self, ctx:SimpleLangParser.MulDivContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#AddSub.
    def enterAddSub(self, ctx:SimpleLangParser.AddSubContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#AddSub.
    def exitAddSub(self, ctx:SimpleLangParser.AddSubContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#Comparison.
    def enterComparison(self, ctx:SimpleLangParser.ComparisonContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#Comparison.
    def exitComparison(self, ctx:SimpleLangParser.ComparisonContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#id.
    def enterId(self, ctx:SimpleLangParser.IdContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#id.
    def exitId(self, ctx:SimpleLangParser.IdContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#Equality.
    def enterEquality(self, ctx:SimpleLangParser.EqualityContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#Equality.
    def exitEquality(self, ctx:SimpleLangParser.EqualityContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#float.
    def enterFloat(self, ctx:SimpleLangParser.FloatContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#float.
    def exitFloat(self, ctx:SimpleLangParser.FloatContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#int.
    def enterInt(self, ctx:SimpleLangParser.IntContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#int.
    def exitInt(self, ctx:SimpleLangParser.IntContext):
        pass



del SimpleLangParser