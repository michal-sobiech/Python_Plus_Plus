from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.operator_terms.DotTerm import DotTerm

from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_nested_expression_term():
    '''
    (a);
    '''

    tokens = [
        NoValToken(TokenType.PARENTHESES_LEFT,  PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 2)),
        NoValToken(TokenType.PARENTHESES_RIGHT, PositionInCode(1, 3)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 4)),
    ]

    a_token = tokens[1]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        expected_ast = Code(
            [Identifier(
                a_token.position,
                a_token.value
            )]
        )
        assert expected_ast == actual_ast
