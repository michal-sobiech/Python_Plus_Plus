from textwrap import dedent

from io import StringIO

from project.lexer.Lexer import Lexer

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.SpecialToken import SpecialToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.code_source.CodeSource import CodeSource

from project.interpreter.ErrorHandler import ErrorHandler


def test_lexing_on_lexed_file():
    code = dedent('''\
    i = 1;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'i',  PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,           PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, 1,   PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,        PositionInCode(1, 6)),
        SpecialToken(TokenType.END_OF_FILE,    PositionInCode(2, 1)),
        SpecialToken(TokenType.END_OF_FILE,    PositionInCode(2, 1)),
        SpecialToken(TokenType.END_OF_FILE,    PositionInCode(2, 1)),
        SpecialToken(TokenType.END_OF_FILE,    PositionInCode(2, 1)),
        SpecialToken(TokenType.END_OF_FILE,    PositionInCode(2, 1)),
    ]

    fake_file_handle = StringIO(code)
    code_source = CodeSource(fake_file_handle)
    lexer = Lexer(code_source, ErrorHandler())

    actual_tokens = [lexer.get_next_token()
                     for _ in range(len(expected_tokens))]

    assert actual_tokens == expected_tokens


def test_get_current_token():
    code = dedent('''\
    i = 1;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'i',  PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,           PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, 1,   PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,        PositionInCode(1, 6)),
    ]

    fake_file_handle = StringIO(code)
    code_source = CodeSource(fake_file_handle)
    lexer = Lexer(code_source, ErrorHandler())

    for i in range(len(expected_tokens)):
        lexer.get_next_token()
        assert expected_tokens[i] == lexer.get_current_token()


def test_lexer_get_current_token_pos():
    code = dedent('''\
    i = 1;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'i',  PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,           PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, '1', PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,        PositionInCode(1, 6)),
    ]

    fake_file_handle = StringIO(code)
    code_source = CodeSource(fake_file_handle)
    lexer = Lexer(code_source, ErrorHandler())

    for i in range(len(expected_tokens)):
        lexer.get_next_token()
        token = lexer.get_current_token()
        token_pos = lexer.get_current_token_pos()

        assert token.position == token_pos
