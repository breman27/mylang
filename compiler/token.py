from enum import Enum, auto


class TokenType(Enum):
    """
    Token types for the tokenizer.
    """

    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    SYMBOL = auto()
    EOF = auto()


class Token:
    """
    A token class to represent a token in the input string.
    """

    def __init__(self, type: TokenType, lexeme: str, literal_value: str = None):
        """
        Initialize a token with its type, lexeme, and optional literal value.
        """
        self.type = type
        self.lexeme = lexeme
        self.value = literal_value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
