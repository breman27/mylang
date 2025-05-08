"""Abstract Syntax Tree (AST) for the language."""


class Expr:
    pass


class Number(Expr):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class Binary(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Binary({self.left}, {self.operator}, {self.right})"
