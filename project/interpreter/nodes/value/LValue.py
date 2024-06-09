from __future__ import annotations
from project.interpreter.nodes.value.ValueType import ValueType
from project.interpreter.nodes.ValueContainerABC import ValueContainerABC
# from project.interpreter.nodes.variable.Variable import Variable


class LValue(ValueContainerABC):
    def __init__(
        self,
        type: ValueType,
        value
    ) -> None:
        super().__init__(type, value)

    def __eq__(self, other: LValue) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return (
            self.type == other.type
            and self.value == other.value
        )

    def __str__(self) -> str:
        match self.type:
            case (ValueType.BOOL | ValueType.INT | ValueType.FLOAT):
                return str(self.value)

            case ValueType.STRING:
                return self.value

            case ValueType.LIST:
                ret = '['
                for i, element in enumerate(self.value.elements):
                    ret += str(element)
                    if i != len(self.value.elements) - 1:
                        ret += ', '
                ret += ']'
                return ret

            case ValueType.DICT:
                ret = '{'
                for i, pair in enumerate(self.value.elements):
                    ret += f'{str(pair[0])}: {str(pair[1])}'
                    if i != len(self.value.elements) - 1:
                        ret += ', '
                ret += '}'
                return ret

            case ValueType.PAIR:
                key_str, value_str = str(self.value.key), str(self.value.value)
                return '{%s, %s}' % (key_str, value_str)

            case ValueType.FUNCTION_NAME:
                return self.value

            case ValueType.NONE:
                return 'None'
