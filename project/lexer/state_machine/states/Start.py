from __future__ import annotations
from project.lexer.state_machine.states.State import State
from project.token.TokenType import TokenType

from project.token.SpecialToken import SpecialToken

from project.lexer.state_machine.states.BareChars import BareChars
from project.lexer.state_machine.states.DotsAndColons import DotsAndColons
from project.lexer.state_machine.states.End import End
from project.lexer.state_machine.states.Grouping import Grouping
from project.lexer.state_machine.states.InsideString import InsideString
from project.lexer.state_machine.states.IntFirstCharNonzero import (
    IntFirstCharNonzero
)
from project.lexer.state_machine.states.IntFirstCharZero import (
    IntFirstCharZero
)
from project.lexer.state_machine.states.Operator import Operator
from project.lexer.state_machine.states.Comment import Comment


class Start(State):
    __slots__ = []

    def __init__(self, context) -> None:
        super().__init__(context)

    def _handle_string_char(self, event: str) -> None:
        self.context.token_type = TokenType.STRING_LITERAL
        self.context.switch_state(InsideString(self.context))

    def _handle_digit(self, event: str) -> None:
        if event == '0':
            self.context.switch_state(IntFirstCharZero(self.context))
        else:
            self.context.switch_state(IntFirstCharNonzero(self.context))
        self.context.token_type = TokenType.INT_LITERAL

    def _handle_operator(self, event: str) -> None:
        self.context.switch_state(Operator(self.context))

    def _handle_grouping_char(self, event: str) -> None:
        match event:
            case self.context.parentheses_left:
                token_type = TokenType.PARENTHESES_LEFT
            case self.context.parentheses_right:
                token_type = TokenType.PARENTHESES_RIGHT

            case self.context.brackets_left:
                token_type = TokenType.BRACKETS_LEFT
            case self.context.brackets_right:
                token_type = TokenType.BRACKETS_RIGHT

            case self.context.braces_left:
                token_type = TokenType.BRACES_LEFT
            case self.context.braces_right:
                token_type = TokenType.BRACES_RIGHT

        self.context.token_type = token_type
        self.context.switch_state(Grouping(self.context))

    def _handle_interpunction(self, event: str) -> None:
        token_type: TokenType
        match event:
            case self.context.end_of_instruction:
                token_type = TokenType.SEMICOLON
            case self.context.comma:
                token_type = TokenType.COMMA
            case self.context.colon:
                token_type = TokenType.COLON
            case self.context.dot:
                token_type = TokenType.DOT
        self.context.token_type = token_type
        self.context.switch_state(DotsAndColons(self.context))

    def _handle_bare_chars(self, event: str) -> None:
        self.context.switch_state(BareChars(self.context))

    def _handle_whitespaces(self, event: str) -> None:
        pass

    def _handle_end_of_file(self, event: str) -> None:
        self.context.token_type = TokenType.END_OF_FILE
        self.context.switch_state(End(self.context))

    def _handle_comment_char(self, event: str) -> None:
        self.context.switch_state(Comment(self.context))

    def _can_start_a_token(self, event: str) -> bool:
        return not (
            event in self.context.get_whitespaces()
            or event == self.context.end_of_file
            or event == self.context.comment_char
        )

    def trigger(self, event: str) -> None:
        if (
            self._can_start_a_token(event)
            and event != self.context.string_char
        ):
            if event.isdigit():
                self._handle_digit(event)

            elif event in self.context.get_operators():
                self._handle_operator(event)

            elif event in self.context.get_grouping_chars():
                self._handle_grouping_char(event)

            elif event in self.context.get_interpunction():
                self._handle_interpunction(event)

            else:
                self._handle_bare_chars(event)

            self.context.char_list.append(event)
            self.context.set_current_token_pos()

        elif event == self.context.string_char:
            self._handle_string_char(event)
            self.context.set_current_token_pos()

        else:
            if event in self.context.get_whitespaces():
                self._handle_whitespaces(event)

            elif event == self.context.end_of_file:
                self._handle_end_of_file(event)
                self.context.set_current_token_pos()

            elif event == self.context.comment_char:
                self._handle_comment_char(event)
