from __future__ import annotations

from project.lexer.state_machine.states.State import State


class Comment(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        if event in [self.context.newline, self.context.end_of_file]:
            self.context.reset_state_machine()
