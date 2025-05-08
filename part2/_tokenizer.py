from _token import Token, TokenType
from grammar import *


class Tokenizer:
    """
    A simple tokenizer that converts a string into a list of tokens.

    source: str - The input string to be tokenized.
    tokens: list - A list of tokens generated from the input string.
    start: int - The starting index of the current token.
    current: int - The current index in the input string.

    """

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0

    def scan_tokens(self):
        """Scan the input string and generate a list of tokens."""

        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None))
        return self.tokens

    def _is_at_end(self):
        """Check if the current position is at the end of the input string."""
        return self.current >= len(self.source)

    def _scan_token(self):
        """Scan the next token from the input string."""
        c = self.source[self.current]
        self.current += 1

        # Check the character and determine the token type
        # For example, if the character is a digit, we create a NUMBER token
        # This will grow as we add more token types
        if is_digit(c):
            self._number()
        elif is_symbol(c):
            token_type = get_symbol_type(c)

            two = c + self.source[self.current : self.current + 1]
            if is_two_char_symbol(two):
                token_type = get_two_char_symbol_type(two)
                self.current += 1
                c = two
            else:
                token_type = get_symbol_type(c)

            if token_type is None:
                raise SyntaxError(f"Unrecognized symbol: {c!r}")

            self.tokens.append(Token(TokenType(token_type), c))
        elif is_whitespace(c):
            pass  # skip whitespace
        else:
            raise SyntaxError(f"Unexpected character: {c}")

    def _number(self):
        # Advance the current position until we reach a non-digit character
        while not self._is_at_end() and self.source[self.current].isdigit():
            self.current += 1

        lexeme = self.source[
            self.start : self.current
        ]  # the lexeme is the substring from start to current (For example, "123" in "123 + 456")

        value = int(lexeme)
        self.tokens.append(Token(TokenType.NUMBER, lexeme, value))


if __name__ == "__main__":
    tokenizer = Tokenizer("(123 + 456) - 789 + 10 ** 2 / 3")
    tokens = tokenizer.scan_tokens()
    for token in tokens:
        print(token)
