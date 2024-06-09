from project.interpreter.InterpreterError import InterpreterError
from project.interpreter.InterpreterErrorMsg import InterpreterErrorMsg
from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg
from project.parser.exceptions.SyntaxError import SyntaxError
from project.parser.exceptions.SyntaxErrorMsg import SyntaxErrorMsg


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# TODO kolory :D


class ErrorHandler:
    def __init__(self) -> None:
        pass

    def handle_lexer_error(self, error: TokenError) -> None:
        msg = (
            'Lexer error at line {}, column {}: {}.\n'
        ).format(
            error.position.row_no,
            error.position.column_no,
            error.error_code.value
        )
        print(msg)
        exit()

    def handle_parser_error(self, error: SyntaxError) -> None:
        msg = (
            'Syntax error at line {}, column {}: {}.\n'
        ).format(
            error.position.row_no,
            error.position.column_no,
            error.code.value
        )
        print(msg)
        exit()

    def handle_interpreter_error(self, error: InterpreterError) -> None:
        msg = (
            'InterpreterError at line {}, column {}: {}.\n'
            'Call stack:\n'
        ).format(
            error.position.row_no,
            error.position.column_no,
            error.description.value
        )
        if len(error.function_call_contexts) > 0:
            for context in reversed(error.function_call_contexts):
                msg += '{} at line {}\n'.format(
                    context.function_name,
                    context.position.row_no
                )
        else:
            msg += '(Empty)\n'
        print(msg)
        exit()
