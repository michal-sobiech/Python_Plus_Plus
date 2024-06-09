from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.linq.LinqQuery import LinqQuery

from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_linq_parsing():
    '''
    from tuple in dict where a orderby func select tuple;
    '''

    tokens = [
        NoValToken(TokenType.FROM,                  PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'tuple',   PositionInCode(1, 6)),
        NoValToken(TokenType.IN,                    PositionInCode(1, 12)),
        ValueToken(TokenType.IDENTIFIER, 'dict',    PositionInCode(1, 15)),
        NoValToken(TokenType.WHERE,                 PositionInCode(1, 20)),
        ValueToken(TokenType.IDENTIFIER, 'a',       PositionInCode(1, 26)),
        NoValToken(TokenType.ORDERBY,               PositionInCode(1, 28)),
        ValueToken(TokenType.IDENTIFIER, 'func',    PositionInCode(1, 36)),
        NoValToken(TokenType.SELECT,                PositionInCode(1, 41)),
        ValueToken(TokenType.IDENTIFIER, 'tuple',   PositionInCode(1, 48)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 53))
    ]

    from_token = tokens[0]
    iterator_var_token = tokens[1]
    source_token = tokens[3]
    condition_token = tokens[5]
    sorting_func_name = tokens[7]
    selected_val_token = tokens[9]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        iterator_var = Identifier(
            iterator_var_token.position,
            iterator_var_token.value
        )

        source = Identifier(
            source_token.position,
            source_token.value
        )

        condition = Identifier(
            condition_token.position,
            condition_token.value
        )

        sorting_func = Identifier(
            sorting_func_name.position,
            sorting_func_name.value
        )

        selected_values = [Identifier(
            selected_val_token.position,
            selected_val_token.value
        )]

        linq_query = LinqQuery(
            from_token.position,
            iterator_var,
            source,
            condition,
            sorting_func,
            selected_values
        )

        expected_ast = Code(
            [linq_query]
        )

        assert actual_ast == expected_ast
