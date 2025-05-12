from _token import TokenType
from abstract_syntax_tree import (
    Expr,
    Number,
    Binary,
    Assignment,
    Variable,
    Unary,
    Definition,
    Call,
)


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def evaluate(self, expr: Expr) -> float:
        if isinstance(expr, Number):
            return expr.value

        if isinstance(expr, Unary):
            right = self.evaluate(expr.operand)
            if expr.operator == TokenType.MINUS:
                return -right
            if expr.operator == TokenType.PLUS:
                return +right

        if isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            if expr.operator == TokenType.PLUS:
                return left + right
            if expr.operator == TokenType.MINUS:
                return left - right
            if expr.operator == TokenType.MULTIPLY:
                return left * right
            if expr.operator == TokenType.DIVIDE:
                return left / right
            if expr.operator == TokenType.EXPONENT:
                return left**right

        if isinstance(expr, Assignment):
            val = self.evaluate(expr.value)
            self.variables[expr.name] = val
            return val

        if isinstance(expr, Variable):
            return self.variables[expr.name]

        if isinstance(expr, Definition):
            self.functions[expr.name] = expr
            return None

        if isinstance(expr, Call):
            function = self.functions.get(expr.callee.name)
            if not function:
                raise RuntimeError(f"Function {expr.callee.name} not defined.")
            if len(expr.arguments) != len(function.params):
                raise RuntimeError(
                    f"Function {expr.callee} takes {len(function.params)} arguments, but got {len(expr.arguments)}."
                )
            arg_vals = [self.evaluate(arg) for arg in expr.arguments]
            local_vars = self.variables.copy()

            self.variables.update(zip(function.params, arg_vals))
            result = self.evaluate(function.body)
            self.variables = local_vars

            return result

        raise RuntimeError(f"Unknown expression: {expr}")
