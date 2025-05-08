from _token import TokenType
from _tokenizer import Tokenizer
from abstract_syntax_tree import Number, Binary


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        """
        expression : addition
        """
        return self.addition()

    def addition(self):
        """
        addition : multiplication ( ( '+' | '-' ) multiplication )*
        """
        expr = self.multiplication()

        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self.multiplication()
            expr = Binary(expr, operator.type, right)

        return expr

    def multiplication(self):
        """
        multiplication : exponent ( ( '*' | '/' ) exponent )*
        """
        expr = self.exponent()

        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self._previous()
            right = self.exponent()
            expr = Binary(expr, operator.type, right)

        return expr

    def exponent(self):
        """
        exponent : factor ( '**' exponent )*
        """
        expr = self.factor()

        while self._match(TokenType.EXPONENT):
            operator = self._previous()
            right = self.exponent()
            expr = Binary(expr, operator.type, right)

        return expr

    def factor(self):
        """
        NUMBER | LEFT_PAREN expression RIGHT_PAREN
        """
        if self._match(TokenType.NUMBER):
            return Number(self._previous().value)
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
