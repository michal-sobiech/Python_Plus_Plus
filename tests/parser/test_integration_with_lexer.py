from textwrap import dedent

from io import StringIO

from project.code_source.CodeSource import CodeSource

from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.function.definition.FunctionDefinition import FunctionDefinition

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_function_and_statement():
    code = dedent('''\
    def a() {}
    b;
    ''')

    error_handler = ErrorHandler()
    parser = Parser(
        Lexer(
            CodeSource(StringIO(code)),
            error_handler
        ),
        error_handler
    )

    actual_ast = parser.parse_code()

    fun_def = FunctionDefinition(
        PositionInCode(1, 1),
        Identifier(
            PositionInCode(1, 5),
            'a'
        ),
        [],
        Block(
            PositionInCode(1, 9),
            []
        )
    )

    statement = Identifier(
        PositionInCode(2, 1),
        'b'
    )

    expected_ast = Code(
        [fun_def, statement]
    )
    assert expected_ast == actual_ast
