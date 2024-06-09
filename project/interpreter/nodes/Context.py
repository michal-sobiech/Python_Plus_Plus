from typing import Optional

from project.interpreter.nodes.value.LValue import LValue

from project.interpreter.nodes.variable.Variable import Variable

from project.interpreter.nodes.Scope import Scope

from itertools import chain

from project.PositionInCode import PositionInCode


class Context:
    def __init__(
        self,
        function_name: str,
        position: PositionInCode
    ) -> None:
        self.function_name = function_name
        self.position = position
        self.scope_stack = [Scope()]

    def add_scope(self) -> None:
        self.scope_stack.append(Scope())

    def pop_scope(self) -> None:
        self.scope_stack.pop()

    def has_variable(self, name: str) -> bool:
        return self.get_variable(name) is not None

    def get_variable(self, name: str) -> Optional[Variable]:
        for scope in reversed(self.scope_stack):
            for var in scope.variables:
                if var.name == name:
                    return var
        return None

    def get_variables(self) -> list[Variable]:
        return list(chain(*[s.variables for s in self.scope_stack]))
