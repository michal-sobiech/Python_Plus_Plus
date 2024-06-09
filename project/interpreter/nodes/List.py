from __future__ import annotations

from project.interpreter.nodes.StructABC import StructABC
from project.interpreter.nodes.function.EmbeddedFunction import EmbeddedFunction
from project.interpreter.nodes.variable.Variable import Variable
from project.interpreter.nodes.value.LValue import LValue
from project.interpreter.nodes.value.ValueType import ValueType


class List(StructABC):
    def __init__(
        self,
        elements: list[LValue]
    ) -> None:
        super().__init__()
        self.elements = elements

    def __eq__(self, other: List) -> bool:
        return self.elements == other.elements
