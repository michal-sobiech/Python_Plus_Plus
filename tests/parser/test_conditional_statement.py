from unittest.mock import patch

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.ast_nodes.conditional_statements.ConditionalStatement import ConditionalStatement
from project.parser.ast_nodes.conditional_statements.ElifStatement import ElifStatement
from project.parser.ast_nodes.conditional_statements.ElseStatement import ElseStatement
from project.parser.ast_nodes.conditional_statements.IfStatement import IfStatement

from project.parser.ast_nodes.Block import Block
from project.parser.ast_nodes.Code import Code
from project.parser.ast_nodes.Identifier import Identifier

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_if_many_elif_else_parsing():
    '''
    if a {}
    elif b {}
    elif c {}
    else {}
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1)),

        NoValToken(TokenType.ELIF,                      PositionInCode(4, 1)),
        ValueToken(TokenType.IDENTIFIER, 'b',           PositionInCode(4, 6)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(4, 8)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(6, 1)),

        NoValToken(TokenType.ELIF,                      PositionInCode(4, 1)),
        ValueToken(TokenType.IDENTIFIER, 'c',           PositionInCode(4, 6)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(4, 8)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(6, 1)),

        NoValToken(TokenType.ELSE,                      PositionInCode(7, 1)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(7, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(9, 1))
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]

    elif_1_token = tokens[4]
    elif_1_condition_token = tokens[5]
    elif_1_body_token = tokens[6]

    elif_2_token = tokens[8]
    elif_2_condition_token = tokens[9]
    elif_2_body_token = tokens[10]

    else_token = tokens[12]
    else_body_token = tokens[13]

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

        elif_1_condition = Identifier(
            elif_1_condition_token.position,
            elif_1_condition_token.value
        )

        elif_1_body = Block(
            elif_1_body_token.position,
            []
        )

        elif_1_statement = ElifStatement(
            elif_1_token.position,
            elif_1_condition,
            elif_1_body
        )

        elif_2_condition = Identifier(
            elif_2_condition_token.position,
            elif_2_condition_token.value
        )

        elif_2_body = Block(
            elif_2_body_token.position,
            []
        )

        elif_2_statement = ElifStatement(
            elif_2_token.position,
            elif_2_condition,
            elif_2_body
        )

        else_body = Block(
            else_body_token.position,
            []
        )

        else_statement = ElseStatement(
            else_token.position,
            else_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [elif_1_statement, elif_2_statement],
            else_statement
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast


def test_if_elif_else_parsing():
    '''
    if a {}
    elif b {}
    else {}
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1)),

        NoValToken(TokenType.ELIF,                      PositionInCode(4, 1)),
        ValueToken(TokenType.IDENTIFIER, 'b',           PositionInCode(4, 6)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(4, 8)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(6, 1)),

        NoValToken(TokenType.ELSE,                      PositionInCode(7, 1)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(7, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(9, 1))
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]

    elif_1_token = tokens[4]
    elif_1_condition_token = tokens[5]
    elif_1_body_token = tokens[6]

    else_token = tokens[8]
    else_body_token = tokens[9]

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

        elif_1_condition = Identifier(
            elif_1_condition_token.position,
            elif_1_condition_token.value
        )

        elif_1_body = Block(
            elif_1_body_token.position,
            []
        )

        elif_1_statement = ElifStatement(
            elif_1_token.position,
            elif_1_condition,
            elif_1_body
        )

        else_body = Block(
            else_body_token.position,
            []
        )

        else_statement = ElseStatement(
            else_token.position,
            else_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [elif_1_statement],
            else_statement
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast


def test_if_else_parsing():
    '''
    if a {}
    else {}
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1)),

        NoValToken(TokenType.ELSE,                      PositionInCode(7, 1)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(7, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(9, 1))
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]

    else_token = tokens[4]
    else_body_token = tokens[5]

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

        else_body = Block(
            else_body_token.position,
            []
        )

        else_statement = ElseStatement(
            else_token.position,
            else_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [],
            else_statement
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast


def test_if_elif_parsing():
    '''
    if a {}
    elif b {}
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1)),

        NoValToken(TokenType.ELIF,                      PositionInCode(4, 1)),
        ValueToken(TokenType.IDENTIFIER, 'b',           PositionInCode(4, 6)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(4, 8)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(6, 1)),
    ]

    if_token = tokens[0]
    if_condition_token = tokens[1]
    if_body_token = tokens[2]

    elif_1_token = tokens[4]
    elif_1_condition_token = tokens[5]
    elif_1_body_token = tokens[6]

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

        elif_1_condition = Identifier(
            elif_1_condition_token.position,
            elif_1_condition_token.value
        )

        elif_1_body = Block(
            elif_1_body_token.position,
            []
        )

        elif_1_statement = ElifStatement(
            elif_1_token.position,
            elif_1_condition,
            elif_1_body
        )

        conditional_statement = ConditionalStatement(
            if_token.position,
            if_statement,
            [elif_1_statement],
            None
        )

        expected_ast = Code(
            [conditional_statement]
        )

        assert expected_ast == actual_ast


def test_if_parsing():
    '''
    if a {}
    '''

    tokens = [
        NoValToken(TokenType.IF,                        PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 4)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(1, 6)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(3, 1))
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
