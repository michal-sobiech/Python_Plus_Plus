from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.literal.BoolLiteral import BoolLiteral
from project.parser.ast_nodes.literal.IntLiteral import IntLiteral
from project.parser.ast_nodes.literal.StringLiteral import StringLiteral

from project.parser.ast_nodes.Code import Code

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_bool_true():
    '''
    True;
    '''

    tokens = [
        NoValToken(TokenType.TRUE,          PositionInCode(1, 1)),
        NoValToken(TokenType.SEMICOLON,     PositionInCode(1, 5))
    ]

    boolean_val = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [BoolLiteral(
                boolean_val.position,
                True
            )]
        )
        assert expected_ast == actual_ast


def test_bool_false():
    '''
    False;
    '''

    tokens = [
        NoValToken(TokenType.FALSE,         PositionInCode(1, 1)),
        NoValToken(TokenType.SEMICOLON,     PositionInCode(1, 6))
    ]

    boolean_val = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [BoolLiteral(
                boolean_val.position,
                False
            )]
        )
        assert expected_ast == actual_ast


def test_int():
    '''
    123;
    '''

    tokens = [
        ValueToken(TokenType.INT_LITERAL, 123, PositionInCode(1, 1)),
        NoValToken(TokenType.SEMICOLON,        PositionInCode(1, 4))
    ]

    int_value = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [IntLiteral(
                int_value.position,
                int_value.value
            )]
        )
        assert expected_ast == actual_ast


def test_string():
    '''
    'test';
    '''

    tokens = [
        ValueToken(TokenType.STRING_LITERAL, 'test', PositionInCode(1, 1)),
        NoValToken(TokenType.SEMICOLON,              PositionInCode(1, 7))
    ]

    string_value = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [StringLiteral(
                string_value.position,
                string_value.value
            )]
        )
        assert expected_ast == actual_ast
