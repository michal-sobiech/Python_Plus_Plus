from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.Assignment import Assignment
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_assignment():
    '''
    a = b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 6)),
    ]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        error_handler = ErrorHandler()
        parser = Parser(Lexer(None, error_handler), error_handler)

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [Assignment(
                tokens[0].position,
                Identifier(
                    tokens[0].position,
                    tokens[0].value
                ),
                Identifier(
                    tokens[2].position,
                    tokens[2].value
                )
            )]
        )
        assert expected_ast == actual_ast
