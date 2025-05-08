from enum import Enum, auto
from typing import Any


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

    def __init__(self, type: TokenType, lexeme: str, value: Any = None):
        """
        Initialize a token with its type, lexeme, and optional literal value.
        """
        self.type = type
        self.lexeme = lexeme
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
