from _token import TokenType
from abstract_syntax_tree import Expr, Number, Binary, Assignment, Variable, Unary


class Interpreter:
    def __init__(self):
        self.variables = {}

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

        raise RuntimeError(f"Unknown expression: {expr}")
