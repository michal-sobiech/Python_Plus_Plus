from enum import Enum, auto


class TokenType(Enum):
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()

    EQUALS = auto()

    PLUS = auto()
    PLUS_PLUS = auto()
    MINUS = auto()
    MINUS_MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    LESS = auto()
    LESS_EQUALS = auto()
    GREATER = auto()
    GREATER_EQUALS = auto()
    EQUALS_EQUALS = auto()

    OR = auto()
    AND = auto()
    NOT = auto()

    DEF = auto()
    RETURN = auto()
    FOR = auto()
    IN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FROM = auto()
    WHERE = auto()
    SELECT = auto()
    ORDERBY = auto()
    TRUE = auto()
    FALSE = auto()
    NONE = auto()
    WHILE = auto()

    PARENTHESES_LEFT = auto()
    PARENTHESES_RIGHT = auto()
    BRACKETS_LEFT = auto()
    BRACKETS_RIGHT = auto()
    BRACES_LEFT = auto()
    BRACES_RIGHT = auto()

    IDENTIFIER = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()

    # Special tokens
    END_OF_FILE = auto()


def token_needs_value(type: TokenType) -> bool:
    return type in [
        TokenType.INT_LITERAL,
        TokenType.FLOAT_LITERAL,
        TokenType.STRING_LITERAL,
        TokenType.IDENTIFIER
    ]


def token_is_special(type: TokenType) -> bool:
    return type == TokenType.END_OF_FILE
