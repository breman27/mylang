import unittest
from _tokenizer import Tokenizer
from _token import TokenType


class TestTokenizer(unittest.TestCase):
    def test_single_number(self):
        tokens = Tokenizer("123").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, "123")
        self.assertEqual(tokens[0].value, 123)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_simple_expression(self):
        tokens = Tokenizer("1+2").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].type, TokenType.PLUS)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_whitespace(self):
        tokens = Tokenizer("  7   -  4 ").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].type, TokenType.MINUS)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_parentheses(self):
        tokens = Tokenizer("(8)").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].type, TokenType.RIGHT_PAREN)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

    def test_unrecognized_symbol(self):
        with self.assertRaises(SyntaxError):
            Tokenizer("$").scan_tokens()


if __name__ == "__main__":
    unittest.main()
