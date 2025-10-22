from MiniLangVisitor import MiniLangVisitor
from MiniLangParser import MiniLangParser


class InterpreterVisitor(MiniLangVisitor):
    def __init__(self):
        # Memoria para variables
        self.memory = {}

    def visitProgram(self, ctx):
        # Ejecuta todas las sentencias
        return self.visitChildren(ctx)

    def visitAssign(self, ctx):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[name] = value
        return value

    def visitPrint(self, ctx):
        value = self.visit(ctx.expr())
        print(value)
        return value

    def visitExpr(self, ctx):
        # Maneja INT
        if ctx.INT() is not None:
            return int(ctx.INT().getText())

        # Maneja ID (variable)
        if ctx.ID() is not None:
            var_name = ctx.ID().getText()
            if var_name not in self.memory:
                raise NameError(f"Variable '{var_name}' no definida")
            return self.memory[var_name]
        
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '(':
            return self.visit(ctx.expr(0))

        if len(ctx.expr()) >= 2:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            # obtener operador seguro
            op = None
            if hasattr(ctx, 'op') and ctx.op is not None:
                # ctx.op es un Token
                op = ctx.op.text
            else:
                op = ctx.getChild(1).getText()

            if op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise ValueError('División por cero')
                return left / right
            elif op == '+':
                return left + right
            elif op == '-':
                return left - right

        # Por defecto, visita hijos
        return self.visitChildren(ctx)