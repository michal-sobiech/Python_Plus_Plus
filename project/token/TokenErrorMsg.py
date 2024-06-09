from enum import Enum


class TokenErrMsg(Enum):
    STR_EOF_INSIDE = 'The file ended during the creation of a string token'
    STR_INVALID_CHAR_AFTER_SLASH = 'Invalid char after slash'
    CHAR_AFTER_STR_END = 'Chars were given after string definition'
    FLOAT_INVALID_CHAR = 'Invalid char inside a float literal definition'
    NUMBER_INVALID_CHAR = 'Invalid char inside a number (int/float) definition'
    INT_DIGIT_AFTER_ZERO = 'A digit was placed after zero'
    INVALID_CHAR_AFTER_SLASH = 'Invalid char after slash'
