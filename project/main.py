import os
import sys

sys.path.append(os.getcwd())

from project.code_source.CodeSource import CodeSource

from project.lexer.Lexer import Lexer

from project.parser.Parser import Parser

from project.interpreter.Interpreter import Interpreter

from project.interpreter.ErrorHandler import ErrorHandler


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('No source file.')
        exit(1)

    source_file = sys.argv[1]

    with open(source_file, 'r') as handle:
        code_source = CodeSource(handle)
        error_handler = ErrorHandler()

        parser = Parser(Lexer(code_source, error_handler), error_handler)
        code = parser.parse_code()

        output_stream = sys.stdout
        interpreter = Interpreter(code, output_stream, error_handler)
        interpreter.interpret()
