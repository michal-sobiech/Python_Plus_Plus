from __future__ import annotations

from project.interpreter.nodes.StructABC import StructABC
from project.interpreter.nodes.function.EmbeddedFunction import EmbeddedFunction
from project.interpreter.nodes.variable.Variable import Variable
from project.interpreter.nodes.value.LValue import LValue
from project.interpreter.nodes.value.ValueType import ValueType


class Pair(StructABC):
    def __init__(
        self,
        key: LValue,
        value: LValue
    ) -> None:
        super().__init__()
        self.key = key
        self.value = value

    def __eq__(self, other: Pair) -> bool:
        return (
            self.key == other.key
            and self.value == other.value
        )
