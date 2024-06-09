from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.End import End


class DotsAndColons(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        self.context.leftover_char = event
        self.context.switch_state(End(self.context))
