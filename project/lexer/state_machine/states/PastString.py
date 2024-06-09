from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.End import End

from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg


class PastString(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        if (event in self.context.get_token_ending_chars()):
            self.context.leftover_char = event
            self.context.switch_state(End(self.context))
        else:
            self.raise_error(TokenErrMsg.CHAR_AFTER_STR_END)
