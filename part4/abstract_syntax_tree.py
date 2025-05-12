"""Abstract Syntax Tree (AST) for the language."""


class Expr:
    pass


class Number(Expr):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"


class Binary(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Binary({self.left}, {self.operator}, {self.right})"


class Unary(Expr):
    def __init__(self, operator: str, operand: Expr):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"Unary({self.operator}, {self.operand})"


class Assignment(Expr):
    def __init__(self, name: str, value: Expr):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"


class Definition(Expr):
    def __init__(self, name: str, params: list[str], body: Expr):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Definition({self.name}, {self.params}, {self.body})"


class Call(Expr):
    def __init__(self, callee: Expr, arguments: list[Expr]):
        self.callee = callee
        self.arguments = arguments

    def __repr__(self):
        return f"Call({self.callee}, {self.arguments})"
