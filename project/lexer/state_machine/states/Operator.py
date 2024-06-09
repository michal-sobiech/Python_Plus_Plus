from __future__ import annotations

from project.lexer.state_machine.states.State import State
from project.lexer.state_machine.states.End import End

from project.token.TokenType import TokenType
from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg


class Operator(State):
    def __init__(self, context) -> None:
        super().__init__(context)

    def trigger(self, event: str) -> None:
        operator_so_far = ''.join(self.context.char_list)
        potential_operator = operator_so_far + event

        if potential_operator in self.context.get_operators():
            # The new char is a part of the operator
            self.context.char_list.append(event)
        else:
            self._decide_on_operator_token_type()
            self.context.leftover_char = event
            self.context.switch_state(End(self.context))

    def _decide_on_operator_token_type(self) -> None:
        token_type: str
        match ''.join(self.context.char_list):
            case self.context.equals:
                token_type = TokenType.EQUALS
            case self.context.plus:
                token_type = TokenType.PLUS
            case self.context.minus:
                token_type = TokenType.MINUS
            case self.context.multiply:
                token_type = TokenType.MULTIPLY
            case self.context.divide:
                token_type = TokenType.DIVIDE
            case self.context.plus_plus:
                token_type = TokenType.PLUS_PLUS
            case self.context.minus_minus:
                token_type = TokenType.MINUS_MINUS
            case self.context.less:
                token_type = TokenType.LESS
            case self.context.less_equals:
                token_type = TokenType.LESS_EQUALS
            case self.context.greater:
                token_type = TokenType.GREATER
            case self.context.greater_equals:
                token_type = TokenType.GREATER_EQUALS
            case self.context.equals_equals:
                token_type = TokenType.EQUALS_EQUALS
            case _:
                self.raise_error(TokenErrMsg.OPERATOR_INVALID_CHAR)

        self.context.token_type = token_type
