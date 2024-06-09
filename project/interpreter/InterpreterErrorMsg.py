from enum import Enum, auto


class InterpreterErrorMsg(Enum):
    STACK_OVERFLOW = 'The call stack has reached its maximum size'
    FUNCTION_ALREADY_EXISTS = 'A function with this name already exists'
    NO_SUCH_FUNCTION = 'No such function'
    INVALID_ARG_COUNT = 'Invalid argument count'
    INVALID_TYPE = 'Invalid type(s)'
    INVALID_VALUE = 'Invalid value(s)'
    NAME_TAKEN_BY_FUNCTION = 'This name is used by an existing function'
    NAME_TAKEN_BY_VAR = 'This name is used by an existing variable'
    NO_SUCH_OBJECT = 'This variable/function does not exist'
    NO_SUCH_RVALUE = 'This is not an rvalue'
    ARG_INVALID_TYPE = 'Argument has invalid type'
    DIVISION_BY_ZERO = 'Division by zero'
    DICT_KEY_EXISTS = 'This key already is in the dictionary'
    NO_SUCH_KEY_IN_DICT = 'This key does not exist'
    DICT_IS_EMPTY = 'This dictionary is empty'
    LIST_IS_EMPTY = 'This list is empty'
    INVALID_INDEX = 'Invalid index'
    UNITERABLE_OBJECT = 'Cannot iterate over this object'
    NO_SUCH_VARIABLE = 'No such variable'
