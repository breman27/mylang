from _token import TokenType
from abstract_syntax_tree import Expr, Number, Binary


class Interpreter:
    def evaluate(self, expr: Expr) -> float:
        if isinstance(expr, Number):
            return expr.value

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

        raise RuntimeError(f"Unknown expression: {expr}")
