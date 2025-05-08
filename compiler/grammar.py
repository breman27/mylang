DIGITS = "0123456789"
SYMBOLS = "+-"
WHITESPACE = " \t\n\r"


def is_digit(c):
    """Check if the character is a digit."""
    return c in DIGITS


def is_symbol(c):
    """Check if the character is a symbol."""
    return c in SYMBOLS


def is_whitespace(c):
    """Check if the character is whitespace."""
    return c in WHITESPACE
