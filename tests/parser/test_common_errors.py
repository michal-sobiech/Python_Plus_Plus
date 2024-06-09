from unittest.mock import patch

import pytest

from project.parser.Parser import Parser

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.parser.exceptions.SyntaxError import SyntaxError
from project.parser.exceptions.SyntaxErrorMsg import SyntaxErrorMsg

from project.interpreter.ErrorHandler import ErrorHandler

from tests.parser.test_utils import get_mocked_get_next_token


def test_no_semicolon():
    '''
    a
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a', PositionInCode(1, 1)),
    ]

    def fake_handle_function(error: SyntaxError):
        raise error

    with (
        patch(
            ('project.interpreter.ErrorHandler.ErrorHandler'
             '.handle_parser_error'),
            side_effect=fake_handle_function
        ),
        patch(
            'project.lexer.Lexer.Lexer.get_next_token',
            side_effect=get_mocked_get_next_token(tokens)
        ),
        pytest.raises(SyntaxError) as err_info
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())
        parser.parse_code()

    assert err_info.value.code == SyntaxErrorMsg.NO_SEMICOLON


def test_fun_call_no_comma():
    '''
    a(b c);
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,  PositionInCode(1, 2)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_RIGHT, PositionInCode(1, 6)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 7)),
    ]

    c_token = tokens[3]

    def fake_handle_function(error: SyntaxError):
        raise error

    with (
        patch(
            ('project.interpreter.ErrorHandler.ErrorHandler'
             '.handle_parser_error'),
            side_effect=fake_handle_function
        ),
        patch(
            'project.lexer.Lexer.Lexer.get_next_token',
            side_effect=get_mocked_get_next_token(tokens)
        ),
        pytest.raises(SyntaxError) as err_info
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())
        parser.parse_code()

    assert (
        err_info.value.code == SyntaxErrorMsg.FUN_NO_RIGHT_PARENTHESES
        and err_info.value.position == c_token.position
    )


def test_invalid_comparison():
    '''
    (b = c);
    '''

    tokens = [
        NoValToken(TokenType.PARENTHESES_LEFT,  PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 2)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 4)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 6)),
        NoValToken(TokenType.PARENTHESES_RIGHT, PositionInCode(1, 7)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 8)),
    ]

    equals_token = tokens[2]

    def fake_handle_function(error: SyntaxError):
        raise error

    with (
        patch(
            ('project.interpreter.ErrorHandler.ErrorHandler'
             '.handle_parser_error'),
            side_effect=fake_handle_function
        ),
        patch(
            'project.lexer.Lexer.Lexer.get_next_token',
            side_effect=get_mocked_get_next_token(tokens)
        ),
        pytest.raises(SyntaxError) as err_info
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())
        parser.parse_code()

        assert True

    assert (
        err_info.value.code == SyntaxErrorMsg.NESTED_EXPR_NO_RIGHT_PARENTHESES
        and err_info.value.position == equals_token.position
    )


def test_unclosed_fun_call_parentheses():
    '''
    a(b;
    '''

    tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,  PositionInCode(1, 2)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 3)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 4)),
    ]

    semicolon_token = tokens[3]

    def fake_handle_function(error: SyntaxError):
        raise error

    with (
        patch(
            ('project.interpreter.ErrorHandler.ErrorHandler'
             '.handle_parser_error'),
            side_effect=fake_handle_function
        ),
        patch(
            'project.lexer.Lexer.Lexer.get_next_token',
            side_effect=get_mocked_get_next_token(tokens)
        ),
        pytest.raises(SyntaxError) as err_info
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())
        parser.parse_code()

        assert True

    assert (
        err_info.value.code == SyntaxErrorMsg.FUN_NO_RIGHT_PARENTHESES
        and err_info.value.position == semicolon_token.position
    )


def test_invalid_fun_name():
    '''
    def 1(a) {}
    '''

    tokens = [
        NoValToken(TokenType.DEF,                     PositionInCode(1, 1)),
        ValueToken(TokenType.INT_LITERAL, 1,          PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,        PositionInCode(1, 6)),
        ValueToken(TokenType.IDENTIFIER, 'a',         PositionInCode(1, 7)),
        NoValToken(TokenType.PARENTHESES_RIGHT,       PositionInCode(1, 8)),
        NoValToken(TokenType.BRACES_LEFT,             PositionInCode(1, 10)),
        NoValToken(TokenType.BRACES_RIGHT,            PositionInCode(1, 11))
    ]

    fun_name_token = tokens[1]

    def fake_handle_function(error: SyntaxError):
        raise error

    with (
        patch(
            ('project.interpreter.ErrorHandler.ErrorHandler'
             '.handle_parser_error'),
            side_effect=fake_handle_function
        ),
        patch(
            'project.lexer.Lexer.Lexer.get_next_token',
            side_effect=get_mocked_get_next_token(tokens)
        ),
        pytest.raises(SyntaxError) as err_info
    ):
        parser = Parser(Lexer(None, None,), ErrorHandler())
        parser.parse_code()

        assert True

    assert (
        err_info.value.code == SyntaxErrorMsg.FUN_INVALID_NAME
        and err_info.value.position == fun_name_token.position
    )
