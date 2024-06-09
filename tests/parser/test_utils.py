from typing import Callable

from project.token.SpecialToken import SpecialToken
from project.token.Token import Token
from project.PositionInCode import PositionInCode
from project.token.TokenType import TokenType


def get_mocked_get_next_token(tokens: list[Token]) -> Callable[[], Token]:
    token_iter = iter(tokens)
    eof_token_pos = PositionInCode(tokens[-1].position.row_no + 1, 1)
    eof_token = SpecialToken(TokenType.END_OF_FILE, eof_token_pos)
    return lambda: next(token_iter, eof_token)
