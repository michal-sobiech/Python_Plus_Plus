from textwrap import dedent

from io import StringIO

from project.lexer.Lexer import Lexer

from project.token.Token import Token

from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode

from project.code_source.CodeSource import CodeSource

from project.interpreter.ErrorHandler import ErrorHandler



def perform_a_lexing_test(
    code: str,
    expected_tokens: list[Token]
) -> None:
    fake_file_handle = StringIO(code)
    code_source = CodeSource(fake_file_handle)
    lexer = Lexer(code_source, ErrorHandler())

    actual_tokens = [lexer.get_next_token()
                     for _ in range(len(expected_tokens))]

    assert actual_tokens == expected_tokens

# ================
# Keywords
# ================


def test_for_loop_lexing():
    code = dedent('''\
    for char in list {
        print(char);
    }
    ''')

    expected_tokens = [
        NoValToken(TokenType.FOR,                   PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'char',    PositionInCode(1, 5)),
        NoValToken(TokenType.IN,                    PositionInCode(1, 10)),
        ValueToken(TokenType.IDENTIFIER, 'list',    PositionInCode(1, 13)),
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 18)),
        ValueToken(TokenType.IDENTIFIER, 'print',   PositionInCode(2, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,      PositionInCode(2, 10)),
        ValueToken(TokenType.IDENTIFIER, 'char',    PositionInCode(2, 11)),
        NoValToken(TokenType.PARENTHESES_RIGHT,     PositionInCode(2, 15)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(2, 16)),
        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(3, 1)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_function_call():
    code = dedent('''\
    func(1, 2, 3);
    func(a, b, c);
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'func',    PositionInCode(1, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,      PositionInCode(1, 5)),
        ValueToken(TokenType.INT_LITERAL, 1,      PositionInCode(1, 6)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 7)),
        ValueToken(TokenType.INT_LITERAL, 2,      PositionInCode(1, 9)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 10)),
        ValueToken(TokenType.INT_LITERAL, 3,      PositionInCode(1, 12)),
        NoValToken(TokenType.PARENTHESES_RIGHT,     PositionInCode(1, 13)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 14)),

        ValueToken(TokenType.IDENTIFIER, 'func',    PositionInCode(2, 1)),
        NoValToken(TokenType.PARENTHESES_LEFT,      PositionInCode(2, 5)),
        ValueToken(TokenType.IDENTIFIER, 'a',       PositionInCode(2, 6)),
        NoValToken(TokenType.COMMA,                 PositionInCode(2, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',       PositionInCode(2, 9)),
        NoValToken(TokenType.COMMA,                 PositionInCode(2, 10)),
        ValueToken(TokenType.IDENTIFIER, 'c',       PositionInCode(2, 12)),
        NoValToken(TokenType.PARENTHESES_RIGHT,     PositionInCode(2, 13)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(2, 14)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_function_definition():
    code = dedent('''\
    def func(val1, val2) {
        return;
    }
    ''')

    expected_tokens = [
        NoValToken(TokenType.DEF,                   PositionInCode(1, 1)),
        ValueToken(TokenType.IDENTIFIER, 'func',    PositionInCode(1, 5)),
        NoValToken(TokenType.PARENTHESES_LEFT,      PositionInCode(1, 9)),
        ValueToken(TokenType.IDENTIFIER, 'val1',    PositionInCode(1, 10)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 14)),
        ValueToken(TokenType.IDENTIFIER, 'val2',    PositionInCode(1, 16)),
        NoValToken(TokenType.PARENTHESES_RIGHT,     PositionInCode(1, 20)),
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 22)),
        NoValToken(TokenType.RETURN,                PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(2, 11)),
        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(3, 1))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_if_elif_else_lexing():
    code = dedent('''\
    variable = 1;
    if variable == 1 {
        variable = 1;
    }
    elif variable == 0 {
        variable = 1;
    }
    else {
        variable = 1;
    }
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'variable',    PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(1, 10)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(1, 12)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(1, 13)),
        NoValToken(TokenType.IF,                        PositionInCode(2, 1)),
        ValueToken(TokenType.IDENTIFIER, 'variable',    PositionInCode(2, 4)),
        NoValToken(TokenType.EQUALS_EQUALS,             PositionInCode(2, 13)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(2, 16)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(2, 18)),
        ValueToken(TokenType.IDENTIFIER, 'variable',    PositionInCode(3, 5)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(3, 14)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(3, 16)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(3, 17)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(4, 1)),

        NoValToken(TokenType.ELIF,                      PositionInCode(5, 1)),
        ValueToken(TokenType.IDENTIFIER, 'variable',    PositionInCode(5, 6)),
        NoValToken(TokenType.EQUALS_EQUALS,             PositionInCode(5, 15)),
        ValueToken(TokenType.INT_LITERAL, 0,            PositionInCode(5, 18)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(5, 20)),
        ValueToken(TokenType.IDENTIFIER, 'variable',    PositionInCode(6, 5)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(6, 14)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(6, 16)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(6, 17)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(7, 1)),

        NoValToken(TokenType.ELSE,                      PositionInCode(8, 1)),
        NoValToken(TokenType.BRACES_LEFT,               PositionInCode(8, 6)),
        ValueToken(TokenType.IDENTIFIER, 'variable',    PositionInCode(9, 5)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(9, 14)),
        ValueToken(TokenType.INT_LITERAL, 1,            PositionInCode(9, 16)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(9, 17)),
        NoValToken(TokenType.BRACES_RIGHT,              PositionInCode(10, 1)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_linq_lexing():
    code = dedent('''\
    result = from tuple in dict
             where tuple.value > 2
             select tuple;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'result',  PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(1, 8)),
        NoValToken(TokenType.FROM,                  PositionInCode(1, 10)),
        ValueToken(TokenType.IDENTIFIER, 'tuple',   PositionInCode(1, 15)),
        NoValToken(TokenType.IN,                    PositionInCode(1, 21)),
        ValueToken(TokenType.IDENTIFIER, 'dict',    PositionInCode(1, 24)),
        NoValToken(TokenType.WHERE,                 PositionInCode(2, 10)),
        ValueToken(TokenType.IDENTIFIER, 'tuple',   PositionInCode(2, 16)),
        NoValToken(TokenType.DOT,                   PositionInCode(2, 21)),
        ValueToken(TokenType.IDENTIFIER, 'value',   PositionInCode(2, 22)),
        NoValToken(TokenType.GREATER,               PositionInCode(2, 28)),
        ValueToken(TokenType.INT_LITERAL, 2,        PositionInCode(2, 30)),
        NoValToken(TokenType.SELECT,                PositionInCode(3, 10)),
        ValueToken(TokenType.IDENTIFIER, 'tuple',   PositionInCode(3, 17)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(3, 22))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_while_loop_lexing():
    code = dedent('''\
    i = 1;
    while True {
        i++;
    }
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'i',       PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 6)),

        NoValToken(TokenType.WHILE,                 PositionInCode(2, 1)),
        NoValToken(TokenType.TRUE,                  PositionInCode(2, 7)),
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(2, 12)),
        ValueToken(TokenType.IDENTIFIER, 'i',       PositionInCode(3, 5)),
        NoValToken(TokenType.PLUS_PLUS,             PositionInCode(3, 6)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(3, 8)),
        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(4, 1))
    ]
    perform_a_lexing_test(code, expected_tokens)


# ================
# Literals
# ================

def test_bool_lexing():
    code = dedent('''\
    a = True;
    b = False;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        NoValToken(TokenType.TRUE,              PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 9)),

        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(2, 3)),
        NoValToken(TokenType.FALSE,             PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(2, 10))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_dict_lexing():
    code = dedent('''\
    a = {
        'a': 1,
        'b': 2,
        'c': 3
    };
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',       PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(1, 3)),
        NoValToken(TokenType.BRACES_LEFT,           PositionInCode(1, 5)),

        ValueToken(TokenType.STRING_LITERAL, 'a',   PositionInCode(2, 5)),
        NoValToken(TokenType.COLON,                 PositionInCode(2, 8)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(2, 10)),
        NoValToken(TokenType.COMMA,                 PositionInCode(2, 11)),

        ValueToken(TokenType.STRING_LITERAL, 'b',   PositionInCode(3, 5)),
        NoValToken(TokenType.COLON,                 PositionInCode(3, 8)),
        ValueToken(TokenType.INT_LITERAL, 2,        PositionInCode(3, 10)),
        NoValToken(TokenType.COMMA,                 PositionInCode(3, 11)),

        ValueToken(TokenType.STRING_LITERAL, 'c',   PositionInCode(4, 5)),
        NoValToken(TokenType.COLON,                 PositionInCode(4, 8)),
        ValueToken(TokenType.INT_LITERAL, 3,        PositionInCode(4, 10)),

        NoValToken(TokenType.BRACES_RIGHT,          PositionInCode(5, 1)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(5, 2))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_float_lexing():
    code = dedent('''\
    a = 0.123;
    b = 1.123;
    c = 0.0;
    d = 1.0;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',           PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(1, 3)),
        ValueToken(TokenType.FLOAT_LITERAL, 0.123,      PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(1, 10)),

        ValueToken(TokenType.IDENTIFIER, 'b',           PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(2, 3)),
        ValueToken(TokenType.FLOAT_LITERAL, 1.123,      PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(2, 10)),

        ValueToken(TokenType.IDENTIFIER, 'c',           PositionInCode(3, 1)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(3, 3)),
        ValueToken(TokenType.FLOAT_LITERAL, 0.0,        PositionInCode(3, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(3, 8)),

        ValueToken(TokenType.IDENTIFIER, 'd',           PositionInCode(4, 1)),
        NoValToken(TokenType.EQUALS,                    PositionInCode(4, 3)),
        ValueToken(TokenType.FLOAT_LITERAL, 1.0,        PositionInCode(4, 5)),
        NoValToken(TokenType.SEMICOLON,                 PositionInCode(4, 8)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_int_lexing():
    code = dedent('''\
    a = 1;
    b = 0;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        ValueToken(TokenType.INT_LITERAL, 1,    PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 6)),

        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(2, 3)),
        ValueToken(TokenType.INT_LITERAL, 0,    PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(2, 6))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_list_lexing():
    code = dedent('''\
    a = [1, 2, 3];
    b = ['1', '2', '3'];
    c = [a, b];
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',       PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(1, 3)),
        NoValToken(TokenType.BRACKETS_LEFT,         PositionInCode(1, 5)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(1, 6)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 7)),
        ValueToken(TokenType.INT_LITERAL, 2,        PositionInCode(1, 9)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 10)),
        ValueToken(TokenType.INT_LITERAL, 3,        PositionInCode(1, 12)),
        NoValToken(TokenType.BRACKETS_RIGHT,        PositionInCode(1, 13)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 14)),

        ValueToken(TokenType.IDENTIFIER, 'b',       PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(2, 3)),
        NoValToken(TokenType.BRACKETS_LEFT,         PositionInCode(2, 5)),
        ValueToken(TokenType.STRING_LITERAL, '1',   PositionInCode(2, 6)),
        NoValToken(TokenType.COMMA,                 PositionInCode(2, 9)),
        ValueToken(TokenType.STRING_LITERAL, '2',   PositionInCode(2, 11)),
        NoValToken(TokenType.COMMA,                 PositionInCode(2, 14)),
        ValueToken(TokenType.STRING_LITERAL, '3',   PositionInCode(2, 16)),
        NoValToken(TokenType.BRACKETS_RIGHT,        PositionInCode(2, 19)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(2, 20)),

        ValueToken(TokenType.IDENTIFIER, 'c',       PositionInCode(3, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(3, 3)),
        NoValToken(TokenType.BRACKETS_LEFT,         PositionInCode(3, 5)),
        ValueToken(TokenType.IDENTIFIER, 'a',       PositionInCode(3, 6)),
        NoValToken(TokenType.COMMA,                 PositionInCode(3, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',       PositionInCode(3, 9)),
        NoValToken(TokenType.BRACKETS_RIGHT,        PositionInCode(3, 10)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(3, 11)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_none_lexing():
    code = dedent('''\
    a = None;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        NoValToken(TokenType.NONE,              PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 9))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_pair_lexing():
    code = dedent('''\
    a = ('a', 1);
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',       PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(1, 3)),
        NoValToken(TokenType.PARENTHESES_LEFT,      PositionInCode(1, 5)),
        ValueToken(TokenType.STRING_LITERAL, 'a',   PositionInCode(1, 6)),
        NoValToken(TokenType.COMMA,                 PositionInCode(1, 9)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(1, 11)),
        NoValToken(TokenType.PARENTHESES_RIGHT,     PositionInCode(1, 12)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(1, 13))
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_string_lexing():
    code = dedent('''\
    a = 'sample';
    b = 'a b';
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',               PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,                        PositionInCode(1, 3)),
        ValueToken(TokenType.STRING_LITERAL, 'sample',      PositionInCode(1, 5)),
        NoValToken(TokenType.SEMICOLON,                     PositionInCode(1, 13)),

        ValueToken(TokenType.IDENTIFIER, 'b',               PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,                        PositionInCode(2, 3)),
        ValueToken(TokenType.STRING_LITERAL, 'a b',         PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,                     PositionInCode(2, 10))
    ]
    perform_a_lexing_test(code, expected_tokens)


# ================
# Operators
# ================

def test_arithmetic_operators_lexing():
    code = dedent('''\
    c = a + b;
    c++;
    c = a - b;
    c--;
    c = a * b;
    c = a / b;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 5)),
        NoValToken(TokenType.PLUS,              PositionInCode(1, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 10)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(2, 1)),
        NoValToken(TokenType.PLUS_PLUS,         PositionInCode(2, 2)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(2, 4)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(3, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(3, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(3, 5)),
        NoValToken(TokenType.MINUS,             PositionInCode(3, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(3, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(3, 10)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(4, 1)),
        NoValToken(TokenType.MINUS_MINUS,       PositionInCode(4, 2)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(4, 4)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(5, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(5, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(5, 5)),
        NoValToken(TokenType.MULTIPLY,          PositionInCode(5, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(5, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(5, 10)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(6, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(6, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(6, 5)),
        NoValToken(TokenType.DIVIDE,            PositionInCode(6, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(6, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(6, 10)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_comparison_operators_lexing():
    code = dedent('''\
    c = a < b;
    c = a <= b;
    c = a > b;
    c = a >= b;
    c = a == b;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 5)),
        NoValToken(TokenType.LESS,              PositionInCode(1, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(1, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 10)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(2, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(2, 5)),
        NoValToken(TokenType.LESS_EQUALS,       PositionInCode(2, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(2, 10)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(2, 11)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(3, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(3, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(3, 5)),
        NoValToken(TokenType.GREATER,           PositionInCode(3, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(3, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(3, 10)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(4, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(4, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(4, 5)),
        NoValToken(TokenType.GREATER_EQUALS,    PositionInCode(4, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(4, 10)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(4, 11)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(5, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(5, 3)),
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(5, 5)),
        NoValToken(TokenType.EQUALS_EQUALS,     PositionInCode(5, 7)),
        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(5, 10)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(5, 11)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_logical_operators_lexing():
    code = dedent('''\
    a = True or False;
    b = True and False;
    c = not True;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'a',   PositionInCode(1, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(1, 3)),
        NoValToken(TokenType.TRUE,              PositionInCode(1, 5)),
        NoValToken(TokenType.OR,                PositionInCode(1, 10)),
        NoValToken(TokenType.FALSE,             PositionInCode(1, 13)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(1, 18)),

        ValueToken(TokenType.IDENTIFIER, 'b',   PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(2, 3)),
        NoValToken(TokenType.TRUE,              PositionInCode(2, 5)),
        NoValToken(TokenType.AND,               PositionInCode(2, 10)),
        NoValToken(TokenType.FALSE,             PositionInCode(2, 14)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(2, 19)),

        ValueToken(TokenType.IDENTIFIER, 'c',   PositionInCode(3, 1)),
        NoValToken(TokenType.EQUALS,            PositionInCode(3, 3)),
        NoValToken(TokenType.NOT,               PositionInCode(3, 5)),
        NoValToken(TokenType.TRUE,              PositionInCode(3, 9)),
        NoValToken(TokenType.SEMICOLON,         PositionInCode(3, 13)),
    ]
    perform_a_lexing_test(code, expected_tokens)


def test_comment_lexing():
    code = dedent('''\
    # This is a comment
    i = 1;
    ''')

    expected_tokens = [
        ValueToken(TokenType.IDENTIFIER, 'i',       PositionInCode(2, 1)),
        NoValToken(TokenType.EQUALS,                PositionInCode(2, 3)),
        ValueToken(TokenType.INT_LITERAL, 1,        PositionInCode(2, 5)),
        NoValToken(TokenType.SEMICOLON,             PositionInCode(2, 6)),
    ]
    perform_a_lexing_test(code, expected_tokens)
