from _token import TokenType

DIGITS = "0123456789"
SYMBOL_MAP = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
}
TWO_CHAR_SYMBOLS = {
    "**": TokenType.EXPONENT,
    "==": TokenType.EQUALS,
}
WHITESPACE = " \t\n\r"


def is_digit(c):
    """Check if the character is a digit."""
    return c in DIGITS


def is_symbol(c):
    """Check if the character is a symbol."""
    return c in SYMBOL_MAP or c in TWO_CHAR_SYMBOLS


def is_two_char_symbol(c):
    """Check if the character is a two-character symbol."""
    return c in TWO_CHAR_SYMBOLS


def get_symbol_type(c):
    """Get the token type for a symbol."""
    return SYMBOL_MAP.get(c, None)


def get_two_char_symbol_type(c):
    """Get the token type for a two-character symbol."""
    return TWO_CHAR_SYMBOLS.get(c, None)


def is_whitespace(c):
    """Check if the character is whitespace."""
    return c in WHITESPACE
