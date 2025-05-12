import unittest
from _tokenizer import Tokenizer
from _token import TokenType
from parser import Parser
from abstract_syntax_tree import Number, Binary, Assignment


class TestParser(unittest.TestCase):
    def test_single_number(self):
        # parsed AST should represent:
        #        123
        tokens = Tokenizer("123").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].lexeme, "123")
        self.assertEqual(tokens[0].value, 123)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

        parser = Parser(tokens)
        expressions = parser.parse()
        # If parse() returns a list, get the first expression
        expression = expressions[0] if isinstance(expressions, list) else expressions

        self.assertIsInstance(expression, Number)
        self.assertEqual(expression.value, 123)

    def test_simple_expression(self):
        # parsed AST should represent:
        #        +
        #      /   \
        #     1     2

        tokens = Tokenizer("1 + 2").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].type, TokenType.PLUS)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

        parser = Parser(tokens)
        expressions = parser.parse()
        expression = expressions[0] if isinstance(expressions, list) else expressions
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator, TokenType.PLUS)
        self.assertIsInstance(expression.left, Number)
        self.assertEqual(expression.left.value, 1)
        self.assertIsInstance(expression.right, Number)
        self.assertEqual(expression.right.value, 2)

    def test_parentheses(self):
        # parsed AST should represent:
        #        *
        #      /   \
        #     +     3
        #    / \
        #   1     2
        #
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
        expressions = parser.parse()
        expression = expressions[0] if isinstance(expressions, list) else expressions

        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator, TokenType.MULTIPLY)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator, TokenType.PLUS)
        self.assertIsInstance(expression.left.left, Number)
        self.assertEqual(expression.left.left.value, 1)
        self.assertIsInstance(expression.left.right, Number)
        self.assertEqual(expression.left.right.value, 2)
        self.assertIsInstance(expression.right, Number)
        self.assertEqual(expression.right.value, 3)

    def test_bad_parentheses(self):
        # parsed AST should raise SyntaxError
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
        expressions = parser.parse()
        expression = expressions[0] if isinstance(expressions, list) else expressions

        # The parsed AST should represent:
        #        +
        #      /   \
        #     7     *
        #          / \
        #         3   /
        #            / \
        #          10   -
        #               / \
        #             /     1
        #           / \
        #         12   +
        #             / \
        #            3   1

        # Check top-level node is Binary(+)
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator, TokenType.PLUS)
        self.assertIsInstance(expression.left, Number)
        self.assertEqual(expression.left.value, 7)

        right = expression.right
        self.assertIsInstance(right, Binary)
        self.assertEqual(right.operator, TokenType.MULTIPLY)
        self.assertIsInstance(right.left, Number)
        self.assertEqual(right.left.value, 3)

        div1 = right.right
        self.assertIsInstance(div1, Binary)
        self.assertEqual(div1.operator, TokenType.DIVIDE)
        self.assertIsInstance(div1.left, Number)
        self.assertEqual(div1.left.value, 10)

        minus = div1.right
        self.assertIsInstance(minus, Binary)
        self.assertEqual(minus.operator, TokenType.MINUS)

        div2 = minus.left
        self.assertIsInstance(div2, Binary)
        self.assertEqual(div2.operator, TokenType.DIVIDE)
        self.assertIsInstance(div2.left, Number)
        self.assertEqual(div2.left.value, 12)

        plus = div2.right
        self.assertIsInstance(plus, Binary)
        self.assertEqual(plus.operator, TokenType.PLUS)
        self.assertIsInstance(plus.left, Number)
        self.assertEqual(plus.left.value, 3)
        self.assertIsInstance(plus.right, Number)
        self.assertEqual(plus.right.value, 1)

        self.assertIsInstance(minus.right, Number)
        self.assertEqual(minus.right.value, 1)

    def test_assignment(self):
        # parsed AST should represent:
        #        =
        #      /   \
        #     x     +
        #          / \
        #         1   2
        tokens = Tokenizer("x = 1 + 2").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.ASSIGN)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.PLUS)
        self.assertEqual(tokens[4].type, TokenType.NUMBER)
        self.assertEqual(tokens[-1].type, TokenType.EOF)

        parser = Parser(tokens)
        expressions = parser.parse()
        expression = expressions[0] if isinstance(expressions, list) else expressions

        self.assertIsInstance(expression, Assignment)
        self.assertEqual(expression.name, "x")
        self.assertIsInstance(expression.value, Binary)
        self.assertEqual(expression.value.operator, TokenType.PLUS)
        self.assertIsInstance(expression.value.left, Number)
        self.assertEqual(expression.value.left.value, 1)
        self.assertIsInstance(expression.value.right, Number)
        self.assertEqual(expression.value.right.value, 2)


if __name__ == "__main__":
    unittest.main()
