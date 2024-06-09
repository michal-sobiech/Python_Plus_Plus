from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.End import End

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from project.lexer.state_machine.StateMachine import StateMachine

from project.token.TokenType import TokenType


class BareChars(State):
    def __init__(self, context: StateMachine) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        if event in self.context.get_token_ending_chars():
            self._decide_on_bare_chars_token_type()
            self.context.leftover_char = event
            self.context.switch_state(End(self.context))
        else:
            self.context.char_list.append(event)

    def _decide_on_bare_chars_token_type(self) -> None:
        token_type: str
        match ''.join(self.context.char_list):
            case self.context.def_keyword:
                token_type = TokenType.DEF
            case self.context.return_keyword:
                token_type = TokenType.RETURN

            case self.context.while_keyword:
                token_type = TokenType.WHILE

            case self.context.for_keyword:
                token_type = TokenType.FOR
            case self.context.in_keyword:
                token_type = TokenType.IN

            case self.context.if_keyword:
                token_type = TokenType.IF
            case self.context.elif_keyword:
                token_type = TokenType.ELIF
            case self.context.else_keyword:
                token_type = TokenType.ELSE

            case self.context.from_keyword:
                token_type = TokenType.FROM
            case self.context.where_keyword:
                token_type = TokenType.WHERE
            case self.context.select_keyword:
                token_type = TokenType.SELECT
            case self.context.orderby_keyword:
                token_type = TokenType.ORDERBY

            case self.context.none_keyword:
                token_type = TokenType.NONE

            case self.context.true_keyword:
                token_type = TokenType.TRUE
            case self.context.false_keyword:
                token_type = TokenType.FALSE

            case self.context.or_keyword:
                token_type = TokenType.OR
            case self.context.and_keyword:
                token_type = TokenType.AND
            case self.context.not_keyword:
                token_type = TokenType.NOT

            case _:
                token_type = TokenType.IDENTIFIER

        self.context.token_type = token_type
