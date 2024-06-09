from abc import abstractmethod

from typing import Callable

from project.interpreter.nodes.function.FunctionABC import FunctionABC


class EmbeddedFunction(FunctionABC):
    def __init__(
        self,
        name: str,
        parameters: list[str],
        function: Callable
    ) -> None:
        super().__init__(name, parameters)
        self.function = function

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_embedded_function(self)
