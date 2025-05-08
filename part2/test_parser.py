import unittest
from _tokenizer import Tokenizer
from _token import TokenType
from parser import Parser, Binary, Number


class TestParser(unittest.TestCase):
    def test_single_number(self):
        tokens = Tokenizer("123").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, "123")
        self.assertEqual(tokens[0].value, 123)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

        parser = Parser(tokens)
        expression = parser.parse()

        self.assertEqual(expression, 123)

    def test_simple_expression(self):
        tokens = Tokenizer("1 + 2").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].type, TokenType.PLUS)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

        parser = Parser(tokens)
        expression = parser.parse()
        self.assertEqual(expression, 3)

    def test_parentheses(self):
        tokens = Tokenizer("(1 + 2) * 3").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].type, TokenType.PLUS)
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[4].type, TokenType.RIGHT_PAREN)
        self.assertEqual(tokens[5].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[6].type, TokenType.NUMBER)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

        parser = Parser(tokens)
        expression = parser.parse()

        self.assertEqual(expression, 9)

    def test_bad_parentheses(self):
        tokens = Tokenizer("(1 + 2 * 3").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].type, TokenType.PLUS)
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[4].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[5].type, TokenType.NUMBER)

        parser = Parser(tokens)
        with self.assertRaises(SyntaxError):
            parser.parse()

    def test_large_complicated_expression(self):
        tokens = Tokenizer("7 + 3 * (10 / (12 / (3 + 1) - 1))").scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        # The expected result of the expression
        expected_result = 7 + 3 * (10 / (12 / (3 + 1) - 1))

        self.assertAlmostEqual(expression, expected_result)


if __name__ == "__main__":
    unittest.main()
