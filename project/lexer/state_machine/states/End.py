from __future__ import annotations

from project.lexer.state_machine.states.State import State


class End(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        pass
