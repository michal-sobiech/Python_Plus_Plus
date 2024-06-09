from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.ForLoop import ForLoop
from project.parser.ast_nodes.Identifier import Identifier
from project.parser.ast_nodes.WhileLoop import WhileLoop

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_for_loop_parsing():
    '''
    for i in list {}
    '''

    tokens = [
        NoValToken(TokenType.FOR,                   PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'i',       PositionInCode(1, 5)),
        NoValToken(TokenType.IN,                    PositionInCode(1, 10)),
        ValueToken(TokenType.IDENTIFIER, 'list',    PositionInCode(1, 13)),
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 18)),
        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(3, 1)),
    ]

    for_token = tokens[0]
    iterator_name = tokens[1]
    sequence_name = tokens[3]
    left_braces = tokens[4]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        iterator = Identifier(iterator_name.position, iterator_name.value)

        sequence = Identifier(
            sequence_name.position,
            sequence_name.value
        )

        body = Block(
            left_braces.position,
            []
        )

        expected_ast = Code(
            [ForLoop(
                for_token.position,
                iterator,
                sequence,
                body
            )]
        )

        assert expected_ast == actual_ast


def test_while_loop_parsing():
    '''
    while a {}
    '''

    tokens = [
        NoValToken(TokenType.WHILE,                    PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER,       'a',    PositionInCode(1, 7)),
        NoValToken(TokenType.BRACES_LEFT,              PositionInCode(1, 9)),
        NoValToken(TokenType.BRACES_RIGHT,             PositionInCode(3, 1))
    ]

    while_token = tokens[0]
    condition_var = tokens[1]
    left_braces = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        condition = Identifier(
            condition_var.position,
            condition_var.value
        )

        body = Block(
            left_braces.position,
            []
        )

        expected_ast = Code(
            [WhileLoop(
                while_token.position,
                condition,
                body
            )]
        )

        assert expected_ast == actual_ast
