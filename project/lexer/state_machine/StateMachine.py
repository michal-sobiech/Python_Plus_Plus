from abc import ABC

from project.lexer.state_machine.states.Start import Start


class StateMachine(ABC):
    __slots__ = ['_state']

    def __init__(self) -> None:
        self._reset_state_machine()

    def reset_state_machine(self):
        self.switch_state(Start(self))

    def switch_state(self, new_state) -> None:
        self._state = new_state
