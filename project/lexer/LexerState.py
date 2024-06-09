from enum import Enum, auto


class LexerState(Enum):
    UNDEFINED = auto()
    INSIDE_STR = auto()
    PAST_STR = auto()

    INT_FIRST_CHAR_NONZERO = auto()
    INT_FIRST_CHAR_ZERO = auto()
    INT_PAST_SECOND_CHAR = auto()
    FLOAT_FIRST_PAST_POINT = auto()
    FLOAT_OTHER_PAST_POINT = auto()

    BARE_CHARS = auto()
    GROUPING = auto()
    BRACES = auto()
    WHITESPACE = auto()
    OPERATOR = auto()
    END_OF_INSTR = auto()
    DOTS_AND_COLONS = auto()
