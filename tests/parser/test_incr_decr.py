from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.incr_decr_statement.DecrementStatement import DecrementStatement
from project.parser.ast_nodes.incr_decr_statement.IncrementStatement import IncrementStatement

from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_incrementation():
    '''
    a++;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.PLUS_PLUS,         PositionInCode(1, 2)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 6)),
    ]

    a_token = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [IncrementStatement(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                )
            )]
        )
        assert expected_ast == actual_ast


def test_decrementation():
    '''
    a--;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.MINUS_MINUS,       PositionInCode(1, 2)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 6)),
    ]

    a_token = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [DecrementStatement(
                a_token.position,
                Identifier(
                    a_token.position,
                    a_token.value
                )
            )]
        )
        assert expected_ast == actual_ast
