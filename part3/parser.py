from _token import Token, TokenType
from _tokenizer import Tokenizer
from abstract_syntax_tree import Number, Binary, Assignment, Variable


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        """
        statement : expression
        """
        if self._check(TokenType.IDENTIFIER) and self._check_next(TokenType.ASSIGN):
            self.current += 1
            name = self._previous().lexeme
            self._consume(TokenType.ASSIGN, "Expect '=' after variable name.")
            value = self.expression()
            return Assignment(name, value)

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
        exponent : unary ( '**' exponent )*
        """
        expr = self.unary()

        while self._match(TokenType.EXPONENT):
            operator = self._previous()
            right = self.exponent()
            expr = Binary(expr, operator.type, right)

        return expr

    def unary(self):
        """
        unary : ( '-' | '+' ) unary | factor
        """
        if self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self.unary()
            # Use a Unary node, or Binary with left as None if Unary not defined
            try:
                from abstract_syntax_tree import Unary

                return Unary(operator.type, right)
            except ImportError:
                return Binary(None, operator.type, right)
        return self.factor()

    def factor(self):
        """
        NUMBER | LEFT_PAREN expression RIGHT_PAREN | VARIABLE
        """
        if self._match(TokenType.NUMBER):
            return Number(self._previous().value)
        elif self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr
        elif self._match(TokenType.IDENTIFIER):
            return Variable(self._previous().lexeme)

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
        if self._is_at_end():
            return False
        return self.tokens[self.current].type == token_type

    def _check_next(self, token_type):
        """Check if the next token is of the given type."""
        if self._is_at_end():
            return False
        return self.tokens[self.current + 1].type == token_type

    def _is_at_end(self):
        """Check if the current position is at the end of the token list."""
        return self.tokens[self.current].type == TokenType.EOF

    def _consume(self, token_type, error_message):
        """Consume the current token if it matches the given type, otherwise raise an error."""
        if self._check(token_type):
            self.current += 1
            return self.tokens[self.current]
        raise SyntaxError(error_message)
