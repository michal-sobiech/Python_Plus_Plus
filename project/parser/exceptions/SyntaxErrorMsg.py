from enum import Enum


class SyntaxErrorMsg(Enum):
    NEITHER_FUN_DEF_NOR_STATEMENT = \
        'Neither a function definition nor a statement'

    FUN_INVALID_NAME = 'Invalid function name'
    FUN_NO_LEFT_PARENTHESES = 'Expected opening parentheses'
    FUN_NO_RIGHT_PARENTHESES = 'Expected closing parentheses'

    FUN_DEF_INVALID_PARAM = 'Invalid function definition parameter'
    FUN_DEF_INVALID_BODY = 'Invalid function definition body'

    FUN_CALL_INVALID_ARG = 'Invalid function call argument'

    BLOCK_NO_RIGHT_BRACES = 'Expected closing braces'

    IF_INVALID_CONDITION = 'Invalid condition of an if statement'
    IF_INVALID_BODY = 'Invalid body of an if statement'
    ELIF_INVALID_CONDITION = 'Invalid condition of an elif statement'
    ELIF_INVALID_BODY = 'Invalid body of an elif statement'
    ELSE_INVALID_BODY = 'Invalid body of an else statement'

    ASSIGN_INVALID_RIGHT_SIDE = 'Invalid right side of an assigment'

    NO_SEMICOLON = 'Expected a semicolon'

    OR_TERM_INVALID_RIGHT_SIDE = 'Invalid right side of the "or" operator'
    AND_TERM_INVALID_RIGHT_SIDE = 'Invalid right side of the "and" operator'
    NOT_TERM_INVALID_RIGHT_SIDE = 'Invalid right side of the "not" operator'
    COMP_TERM_INVALID_RIGHT_SIDE = \
        'Invalid right side of the comparison operator'
    ADD_OR_SUB_TERM_INVALID_RIGHT_SIDE = \
        'Invalid right side of the + or - operator'
    MUL_OR_DIV_TERM_INVALID_RIGHT_SIDE = \
        'Invalid right side of the * or / operator'
    MINUS_TERM_INVALID_RIGHT_SIDE = \
        'Invalid right side of the unary minus operator'
    DOT_TERM_INVALID_TERM = 'Invalid term after the dot'

    LINQ_INVALID_ITERATOR_VAR = 'Invalid iterator variable'
    LINQ_NO_IN = 'Expected "in"'
    LINQ_INVALID_SEQUENCE = 'Invalid sequence'
    LINQ_NO_WHERE = 'Expected "where"'
    LINQ_INVALID_CONDITION = 'Invalid condition'
    LINQ_NO_ORDERBY_FUN = 'No function given after "orderby"'
    LINQ_NO_SELECT = 'Expected "select"'
    LINQ_INVALID_SELECTED_VALUES = 'Invalid selected values'
    LINQ_SELECTED_VALUES_END_WITH_COMMA = \
        'Comma at the end of selected values'

    FOR_LOOP_INVALID_ITERATOR_VAR = 'Invalid iterator variable'
    FOR_LOOP_NO_IN = 'Expected "in"'
    FOR_LOOP_INVALID_SEQUENCE = 'Invalid sequence'
    FOR_LOOP_INVALID_BODY = 'Invalid body'

    WHILE_LOOP_INVALID_CONDITION = 'Invalid condition'
    WHILE_LOOP_INVALID_BODY = 'Invalid body'

    DICT_NO_RIGHT_BRACES = 'Expected closing braces'

    DICT_ELEM_INVALID_VALUE = "Invalid dict element's value"
    DICT_ELEM_NO_COLON = 'Expected a colon'
    INVALID_DICT_ELEM = 'Invalid dict element'

    PAIR_INVALID_VALUE = 'Invalid value of the pair'
    PAIR_NO_RIGHT_BRACES = 'Expected closing braces'

    LIST_INVALID_ELEMENT = 'Invalid list element'
    LIST_NO_RIGHT_BRACKETS = 'Expected closing bracket'

    NESTED_EXPR_INVALID_EXPR = 'Invalid expression'
    NESTED_EXPR_NO_RIGHT_PARENTHESES = 'Expected closing parentheses'
