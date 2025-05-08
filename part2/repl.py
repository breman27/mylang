from interpreter import Interpreter
from _tokenizer import Tokenizer
from parser import Parser

if __name__ == "__main__":
    interpreter = Interpreter()
    while True:
        src = input("> ")
        tokens = Tokenizer(src).scan_tokens()
        ast = Parser(tokens).parse()
        result = interpreter.evaluate(ast)
        print(result)
