from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.function.definition.FunctionDefinition import FunctionDefinition

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_function_and_statement():
    '''
    def a() {}
    b;
    '''

    tokens = [
        NoValToken(TokenType.DEF,                     PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',         PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,        PositionInCode(1, 6)),
        NoValToken(TokenType.PARENTHESES_RIGHT,       PositionInCode(1, 7)),
        NoValToken(TokenType.BRACES_LEFT,             PositionInCode(1, 9)),
        NoValToken(TokenType.BRACES_RIGHT,            PositionInCode(1, 10)),

        ValueToken(TokenType.IDENTIFIER, 'b',         PositionInCode(2, 1)),
        NoValToken(TokenType.SEMICOLON,               PositionInCode(2, 2))
    ]

    def_token = tokens[0]
    a_token = tokens[1]
    left_braces = tokens[4]

    b_token = tokens[6]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        fun_def = FunctionDefinition(
            def_token.position,
            Identifier(
                a_token.position,
                a_token.value
            ),
            [],
            Block(
                left_braces.position,
                []
            )
        )

        statement = Identifier(
            b_token.position,
            b_token.value
        )

        expected_ast = Code(
            [fun_def, statement]
        )
        assert expected_ast == actual_ast
