from typing import Optional

from project.interpreter.nodes.variable.Variable import Variable

from project.interpreter.nodes.value.LValue import LValue

from project.interpreter.nodes.value.ValueType import ValueType


class Scope:
    def __init__(self) -> None:
        self.variables: list[Variable] = []

    def has_variable(self, name: str) -> bool:
        return self.get_variable(name) is not None

    def get_variable(self, name: str) -> Optional[Variable]:
        for var in self.variables:
            if var.name == name:
                return var
        return None
