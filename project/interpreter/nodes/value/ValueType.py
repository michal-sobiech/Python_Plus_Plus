from enum import Enum, auto


class ValueType(Enum):
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    DICT = auto()
    LIST = auto()
    PAIR = auto()
    FUNCTION_NAME = auto()
    NONE = auto()
