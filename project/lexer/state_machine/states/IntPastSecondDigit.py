from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.End import End
from project.lexer.state_machine.states.FloatFirstPastPoint import (
    FloatFirstPastPoint
)

from project.token.TokenType import TokenType
from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg


class IntPastSecondDigit(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        termination_chars = self.context.get_token_ending_chars()
        termination_chars.remove(self.context.dot)

        if event == self.context.dot:
            self.context.token_type = TokenType.FLOAT_LITERAL
            self.context.char_list.append(event)
            self.context.switch_state(FloatFirstPastPoint(self.context))
        if (event in termination_chars):
            self.context.leftover_char = event
            self.context.switch_state(End(self.context))
        elif event.isdigit():
            pass
        else:
            self.raise_error(TokenErrMsg.NUMBER_INVALID_CHAR)
