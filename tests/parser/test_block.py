from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.conditional_statements.ConditionalStatement import ConditionalStatement
from project.parser.ast_nodes.conditional_statements.IfStatement import IfStatement

from project.parser.ast_nodes.literal.IntLiteral import IntLiteral

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_block_with_no_statements():
    '''
    if a {}
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(1, 7))
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        if_condition = Identifier(
            if_condition_token.position,
            if_condition_token.value
        )

        if_body = Block(
            if_body_token.position,
            []
        )

        if_statement = IfStatement(
            if_token.position,
            if_condition,
            if_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [],
            None
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast


def test_block_with_single_statement_parsing():
    '''
    if a {
        1;
    }
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(2, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1))
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]
    if_body_expr_token = tokens[3]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        if_condition = Identifier(
            if_condition_token.position,
            if_condition_token.value
        )

        if_body = Block(
            if_body_token.position,
            [IntLiteral(
                if_body_expr_token.position,
                if_body_expr_token.value
            )]
        )

        if_statement = IfStatement(
            if_token.position,
            if_condition,
            if_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [],
            None
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast


def test_block_with_multiple_statements_parsing():
    '''
    if a {
        1;
        2;
    }
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(2, 6)),
        ValueToken(TokenType.INT_LITERAL, 2,            PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(2, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1))
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]
    if_body_expr_1_token = tokens[3]
    if_body_expr_2_token = tokens[5]

    with patch(
        'project.lexer.Lexer.Lexer.get_next_token',
        side_effect=get_mocked_get_next_token(tokens)
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())

        actual_ast = parser.parse_code()

        if_condition = Identifier(
            if_condition_token.position,
            if_condition_token.value
        )

        if_body = Block(
            if_body_token.position,
            [
                IntLiteral(
                    if_body_expr_1_token.position,
                    if_body_expr_1_token.value
                ),
                IntLiteral(
                    if_body_expr_2_token.position,
                    if_body_expr_2_token.value
                )
            ]
        )

        if_statement = IfStatement(
            if_token.position,
            if_condition,
            if_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [],
            None
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast
