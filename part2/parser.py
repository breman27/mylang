from _token import Token, TokenType


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


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        expr = self.term()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self.term()
            if operator.type == TokenType.PLUS:
                expr = expr + right
            elif operator.type == TokenType.MINUS:
                expr = expr - right

        return expr

    def term(self):
        result = self.factor()

        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self._previous()
            right = self.factor()
            if operator.type == TokenType.MULTIPLY:
                result = result * right
            elif operator.type == TokenType.DIVIDE:
                result = result / right

        return result

    def factor(self):
        if self._match(TokenType.NUMBER):
            return self._previous().value
        elif self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr

    def _match(self, *token_types):
        """Check if the current token matches any of the given token types."""
        for token_type in token_types:
            if self._check(token_type):
                self.current += 1
                return True
        return False

    def _previous(self):
        """Return the previous token."""
        return self.tokens[self.current - 1]

    def _check(self, token_type):
        """Check if the current token is of the given type."""
        return self._is_at_end() or self.tokens[self.current].type == token_type

    def _is_at_end(self):
        """Check if the current position is at the end of the token list."""
        return self.current >= len(self.tokens)

    def _consume(self, token_type, error_message):
        """Consume the current token if it matches the given type, otherwise raise an error."""
        if self._check(token_type):
            self.current += 1
            return self.tokens[self.current]
        raise SyntaxError(error_message)


if __name__ == "__main__":
    # Example usage
    tokens = [
        Token(TokenType.NUMBER, "2", 2),
        Token(TokenType.MULTIPLY, "*"),
        Token(TokenType.NUMBER, "2", 2),
        Token(TokenType.EOF, "", None),
    ]
    parser = Parser(tokens)
    expression = parser.parse()
    print(expression)  # Should print a representation of the parsed expression
