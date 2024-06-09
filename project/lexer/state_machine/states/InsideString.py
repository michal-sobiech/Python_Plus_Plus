from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.PastString import PastString

from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg


class InsideString(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        if event in self.context.end_of_file:
            self.raise_error(TokenErrMsg.STR_EOF_INSIDE)
        else:
            if event == self.context.string_char:
                self.context.switch_state(PastString(self.context))
            elif event == self.context.slash:
                from project.lexer.state_machine.states.InsideStrAfterSlash import InsideStrAfterSlash
                self.context.switch_state(InsideStrAfterSlash(self.context))
            else:
                self.context.char_list.append(event)
