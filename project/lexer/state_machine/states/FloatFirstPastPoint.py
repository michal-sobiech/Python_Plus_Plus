from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.FloatOtherPastPoint import (
    FloatOtherPastPoint
)

from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg


class FloatFirstPastPoint(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        termination_chars = self.context.get_token_ending_chars()
        termination_chars.remove(self.context.dot)

        if event.isdigit():
            self.context.char_list.append(event)
            self.context.switch_state(FloatOtherPastPoint(self.context))
        else:
            self.raise_error(TokenErrMsg.FLOAT_INVALID_CHAR)
