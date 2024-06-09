from __future__ import annotations

from abc import ABC, abstractmethod

from project.interpreter.nodes.value.ValueType import ValueType
# from project.interpreter.nodes.value.LValue import LValue


class ValueContainerABC(ABC):
    @abstractmethod
    def __init__(
        self,
        type: ValueType,
        value
    ) -> None:
        super().__init__()
        self.type = type
        self.value = value
