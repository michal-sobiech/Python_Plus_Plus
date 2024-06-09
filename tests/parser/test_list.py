from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.list.List import List

from project.parser.ast_nodes.literal.IntLiteral import IntLiteral

from project.parser.ast_nodes.Code import Code

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_list_many_elements():
    '''
    [1, 2, 3];
    '''

    tokens = [
        NoValToken(TokenType.BRACKETS_LEFT,         PositionInCode(1, 1)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(1, 2)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, 2,        PositionInCode(1, 5)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 6)),
        ValueToken(TokenType.INT_LITERAL, 3,        PositionInCode(1, 8)),
        NoValToken(TokenType.BRACKETS_RIGHT,        PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 10)),
    ]

    brackets_left = tokens[0]
    first_element = tokens[1]
    second_element = tokens[3]
    third_element = tokens[5]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        elements = [
            IntLiteral(
                first_element.position,
                first_element.value
            ),
            IntLiteral(
                second_element.position,
                second_element.value
            ),
            IntLiteral(
                third_element.position,
                third_element.value
            )
        ]

        collection = List(
            brackets_left.position,
            elements
        )

        expected_ast = Code(
            [collection]
        )

        assert expected_ast == actual_ast


def test_list_one_element():
    '''
    [1];
    '''

    tokens = [
        NoValToken(TokenType.BRACKETS_LEFT,         PositionInCode(1, 1)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(1, 2)),
        NoValToken(TokenType.BRACKETS_RIGHT,        PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 10)),
    ]

    brackets_left = tokens[0]
    first_element = tokens[1]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        elements = [
            IntLiteral(
                first_element.position,
                first_element.value
            )
        ]

        collection = List(
            brackets_left.position,
            elements
        )

        expected_ast = Code(
            [collection]
        )

        assert expected_ast == actual_ast


def test_list_zero_elements():
    '''
    [];
    '''

    tokens = [
        NoValToken(TokenType.BRACKETS_LEFT,         PositionInCode(1, 1)),
        NoValToken(TokenType.BRACKETS_RIGHT,        PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 10)),
    ]

    brackets_left = tokens[0]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        elements = []

        collection = List(
            brackets_left.position,
            elements
        )

        expected_ast = Code(
            [collection]
        )

        assert expected_ast == actual_ast
