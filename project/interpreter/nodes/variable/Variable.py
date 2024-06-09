from project.interpreter.nodes.ValueContainerABC import ValueContainerABC
from project.interpreter.nodes.value.ValueType import ValueType
from project.interpreter.nodes.value.LValue import LValue


class Variable(ValueContainerABC):
    def __init__(
        self,
        name: str,
        type: ValueType,
        value
    ) -> None:
        super().__init__(type, value)
        self.name = name
