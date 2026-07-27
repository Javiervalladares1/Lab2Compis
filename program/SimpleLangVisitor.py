# Generated from SimpleLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleLangParser import SimpleLangParser
else:
    from SimpleLangParser import SimpleLangParser

# This class defines a complete generic visitor for a parse tree produced by SimpleLangParser.

class SimpleLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpleLangParser#prog.
    def visitProg(self, ctx:SimpleLangParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#printExpr.
    def visitPrintExpr(self, ctx:SimpleLangParser.PrintExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#assign.
    def visitAssign(self, ctx:SimpleLangParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#blank.
    def visitBlank(self, ctx:SimpleLangParser.BlankContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#parens.
    def visitParens(self, ctx:SimpleLangParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#bool.
    def visitBool(self, ctx:SimpleLangParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#MulDiv.
    def visitMulDiv(self, ctx:SimpleLangParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#AddSub.
    def visitAddSub(self, ctx:SimpleLangParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#Comparison.
    def visitComparison(self, ctx:SimpleLangParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#id.
    def visitId(self, ctx:SimpleLangParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#Equality.
    def visitEquality(self, ctx:SimpleLangParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#float.
    def visitFloat(self, ctx:SimpleLangParser.FloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#int.
    def visitInt(self, ctx:SimpleLangParser.IntContext):
        return self.visitChildren(ctx)



del SimpleLangParser