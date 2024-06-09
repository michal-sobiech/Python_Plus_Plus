from enum import Enum, auto


class ResultType(Enum):
    LVALUE = auto()
    RETURN = auto()
    COND_STMT_ENTERED = auto()
    OBJECT_NAME = auto()
    BLOCK_EXITED = auto()


class Result():
    def __init__(
        self,
        type: ResultType,
        value
    ) -> None:
        super().__init__()
        self.type = type
        self.value = value
