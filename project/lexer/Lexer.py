from typing import Optional
from copy import deepcopy

import os
import sys

sys.path.append(os.getcwd())

from project.lexer.state_machine.StateMachine import StateMachine

from project.lexer.state_machine.states.End import End

from project.token.Token import Token
from project.token.ValueToken import ValueToken
from project.token.NoValToken import NoValToken
from project.token.SpecialToken import SpecialToken
from project.token.TokenType import (
    TokenType, token_needs_value, token_is_special
)
from project.PositionInCode import PositionInCode

from project.code_source.CodeSource import CodeSource

from project.token.TokenError import TokenError

from project.interpreter.ErrorHandler import ErrorHandler


class Lexer(StateMachine):
    __slots__ = [
        '_error_handler',
        'token_type',
        'char_list',

        'current_token',

        'code_source',

        'leftover_char',

        '_new_token_pos',

        'string_char',

        # 1 char operators
        'plus',
        'minus',
        'equals',
        'greater',
        'less',
        'multiply',
        'divide',

        # 2 char operators
        'equals_equals',
        'greater_equals',
        'less_equals',
        'plus_plus',
        'minus_minus',

        # Grouping operators
        'parentheses_left',
        'parentheses_right',
        'brackets_left',
        'brackets_right',
        'braces_left',
        'braces_right',

        # Keywords
        'def_keyword',
        'return_keyword',

        'while_keyword',

        'for_keyword',
        'in_keyword',

        'if_keyword',
        'elif_keyword',
        'else_keyword',

        'from_keyword',
        'where_keyword',
        'select_keyword',
        'orderby_keyword',

        'none_keyword',

        'true_keyword',
        'false_keyword',

        'or_keyword',
        'and_keyword',
        'not_keyword',

        # Whitespaces
        'space',
        'newline',
        'tab',

        # Interpunction
        'end_of_instruction',
        'comma',
        'colon',
        'dot',

        'end_of_file',

        'comment_char',

        'slash',
        'newline_char',
        'tab_char',
    ]

    def __init__(
        self,
        code_source: CodeSource,
        error_handler: ErrorHandler
    ) -> None:
        self.token_type: TokenType
        self.char_list: list

        self.current_token = None

        self.code_source = code_source

        self._error_handler = error_handler

        self.leftover_char: str = None

        self._new_token_pos: PositionInCode = None

        # Char that starts and ends a string
        self.string_char = "'"

        # 1 char operators
        self.plus = '+'
        self.minus = '-'
        self.equals = '='
        self.greater = '>'
        self.less = '<'
        self.multiply = '*'
        self.divide = '/'

        # 2 char operators
        self.equals_equals = '=='
        self.greater_equals = '>='
        self.less_equals = '<='
        self.plus_plus = '++'
        self.minus_minus = '--'

        # Grouping operators
        self.parentheses_left = '('
        self.parentheses_right = ')'
        self.brackets_left = '['
        self.brackets_right = ']'
        self.braces_left = '{'
        self.braces_right = '}'

        # Keywords
        self.def_keyword = 'def'
        self.return_keyword = 'return'

        self.while_keyword = 'while'

        self.for_keyword = 'for'
        self.in_keyword = 'in'

        self.if_keyword = 'if'
        self.elif_keyword = 'elif'
        self.else_keyword = 'else'

        self.from_keyword = 'from'
        self.where_keyword = 'where'
        self.select_keyword = 'select'
        self.orderby_keyword = 'orderby'

        self.none_keyword = 'None'

        self.true_keyword = 'True'
        self.false_keyword = 'False'

        self.or_keyword = 'or'
        self.and_keyword = 'and'
        self.not_keyword = 'not'

        # Whitespaces
        self.space = ' '
        self.newline = '\n'
        self.tab = '\t'

        # Interpunction
        self.end_of_instruction = ';'
        self.comma = ','
        self.colon = ':'
        self.dot = '.'

        # EOF
        self.end_of_file = '\x03'

        # Comment
        self.comment_char = '#'

        self.slash = '\\'
        self.newline_char = 'n'
        self.tab_char = 't'

    def get_1_char_operators(self) -> list[str]:
        return [
            self.plus,
            self.minus,
            self.equals,
            self.greater,
            self.less,
            self.multiply,
            self.divide,
        ]

    def get_2_char_operators(self) -> list[str]:
        return [
            self.equals_equals,
            self.greater_equals,
            self.less_equals,
            self.plus_plus,
            self.minus_minus,
        ]

    def get_operators(self) -> list[str]:
        return self.get_1_char_operators() + self.get_2_char_operators()

    def get_grouping_chars(self) -> list[str]:
        return [
            self.parentheses_left,
            self.parentheses_right,
            self.brackets_left,
            self.brackets_right,
            self.braces_left,
            self.braces_right
        ]

    def get_keywords(self) -> list[str]:
        return [
            self.def_keyword,
            self.return_keyword,

            self.while_keyword,

            self.for_keyword,
            self.in_keyword,

            self.if_keyword,
            self.elif_keyword,
            self.else_keyword,

            self.from_keyword,
            self.where_keyword,
            self.select_keyword,
            self.orderby_keyword,

            self.none_keyword,

            self.true_keyword,
            self.false_keyword,

            self.or_keyword,
            self.and_keyword,
            self.not_keyword,
        ]

    def get_whitespaces(self) -> list[str]:
        return [
            self.space,
            self.newline,
            self.tab
        ]

    def get_interpunction(self) -> list[str]:
        return [
            self.end_of_instruction,
            self.comma,
            self.colon,
            self.dot
        ]

    def get_token_ending_chars(self) -> list[str]:
        return (
            self.get_whitespaces()
            + self.get_grouping_chars()
            + self.get_operators()
            + self.get_interpunction()
            + [self.end_of_file]
        )

    def prepare_for_new_token(self) -> None:
        super().reset_state_machine()
        self.token_type = None
        self.char_list = []

    def _get_char(self) -> str:
        char: str
        if self.leftover_char:
            char = self.leftover_char
            self.leftover_char = None
        else:
            char = next(self.code_source, self.end_of_file)
        return char

    def set_leftover_char(self, new) -> None:
        self.leftover_char = new

    def get_next_token(self) -> Optional[Token]:
        try:
            self.prepare_for_new_token()

            while type(self._state) is not End:
                char = self._get_char()
                self._state.trigger(char)

            token: Token
            if token_is_special(self.token_type):
                token = SpecialToken(
                    type=self.token_type,
                    position=deepcopy(self._new_token_pos)
                )
            elif token_needs_value(self.token_type):
                token_value = ''.join(self.char_list)
                match self.token_type:
                    case TokenType.INT_LITERAL:
                        token_value = int(token_value)
                    case TokenType.FLOAT_LITERAL:
                        token_value = float(token_value)
                    case _:
                        pass
                token = ValueToken(
                    type=self.token_type,
                    value=token_value,
                    position=deepcopy(self._new_token_pos)
                )
            else:
                token = NoValToken(
                    type=self.token_type,
                    position=deepcopy(self._new_token_pos)
                )
            self.current_token = token
            return token

        except TokenError as error:
            self._error_handler.handle_lexer_error(error)

    def get_current_token(self) -> Optional[Token]:
        return self.current_token

    def get_current_token_pos(self) -> PositionInCode:
        return self.current_token.position

    def set_current_token_pos(self) -> None:
        self._new_token_pos = PositionInCode(
            self.code_source.char_row_no,
            self.code_source.char_column_no
        )
