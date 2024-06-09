from textwrap import dedent

from io import StringIO

from unittest.mock import patch
import pytest

from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg

from project.code_source.CodeSource import CodeSource
from project.lexer.Lexer import Lexer

from project.interpreter.ErrorHandler import ErrorHandler


def perform_a_test_of_lexing_incorrect_code(
    code: str,
    expected_error_msg: TokenErrMsg
) -> None:

    def fake_handle_function(error: TokenError):
        raise error

    with (
        patch(
            ('project.interpreter.ErrorHandler.ErrorHandler'
             '.handle_lexer_error'),
            side_effect=fake_handle_function
        ),
        pytest.raises(TokenError) as error_info
    ):
        fake_file_handle = StringIO(code)
        code_source = CodeSource(fake_file_handle)
        lexer = Lexer(code_source, ErrorHandler())

        while True:
            if lexer.get_next_token() is None:
                break

    assert error_info.value.error_code == expected_error_msg


def test_unclosed_string():
    code = dedent('''\
    a = 'sample text
    ''')

    perform_a_test_of_lexing_incorrect_code(
        code,
        TokenErrMsg.STR_EOF_INSIDE
    )


def test_char_after_str_ended():
    code = dedent('''\
    a = 'sample text'abc
    ''')

    perform_a_test_of_lexing_incorrect_code(
        code,
        TokenErrMsg.CHAR_AFTER_STR_END
    )


def test_invalid_char_in_float():
    code = dedent('''\
    a = 0.1Z34S;
    ''')

    perform_a_test_of_lexing_incorrect_code(
        code,
        TokenErrMsg.FLOAT_INVALID_CHAR
    )


def test_invalid_char_in_int():
    code = dedent('''\
    a = 1Z34S;
    ''')

    perform_a_test_of_lexing_incorrect_code(
        code,
        TokenErrMsg.NUMBER_INVALID_CHAR
    )


def test_digit_after_zero():
    code = dedent('''\
    a = 0123;
    ''')

    perform_a_test_of_lexing_incorrect_code(
        code,
        TokenErrMsg.INT_DIGIT_AFTER_ZERO
    )
