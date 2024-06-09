from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.PastString import PastString

from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg


class InsideStrAfterSlash(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        if event in self.context.end_of_file:
            self.raise_error(TokenErrMsg.STR_EOF_INSIDE)
        else:
            from project.lexer.state_machine.states.InsideString import InsideString
            self.context.switch_state(InsideString(self.context))
            if event in [
                self.context.slash,
                self.context.newline_char,
                self.context.tab_char,
                self.context.string_char
            ]:
                if event == self.context.newline_char:
                    new_char = '\n'
                elif event == self.context.slash:
                    new_char = '\\'
                elif event == self.context.tab_char:
                    new_char = '\t'
                elif event == self.context.string_char:
                    new_char = "'"
                self.context.char_list.append(new_char)
            else:
                self.raise_error(TokenErrMsg.INVALID_CHAR_AFTER_SLASH)
