from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.return_statement.ReturnNoValue import ReturnNoValue
from project.parser.ast_nodes.return_statement.ReturnWithValue import ReturnWithValue

from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_no_value_return():
    '''
    return;
    '''

    tokens = [
        NoValToken(TokenType.RETURN,    PositionInCode(1, 1)),
        NoValToken(TokenType.SEMICOLON, PositionInCode(1, 6)),
    ]

    return_token = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [ReturnNoValue(return_token.position)]
        )
        assert expected_ast == actual_ast


def test_return_with_value():
    '''
    return a;
    '''

    tokens = [
        NoValToken(TokenType.RETURN,          PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 8)),
        NoValToken(TokenType.SEMICOLON,       PositionInCode(1, 9)),
    ]

    return_token = tokens[0]
    a_token = tokens[1]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [ReturnWithValue(
                return_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                )
            )]
        )
        assert expected_ast == actual_ast
