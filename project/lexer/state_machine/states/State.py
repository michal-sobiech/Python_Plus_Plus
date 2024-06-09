from __future__ import annotations

from abc import ABC, abstractmethod

from project.token.TokenError import TokenError
from project.token.TokenErrorMsg import TokenErrMsg
from project.PositionInCode import PositionInCode


class State(ABC):
    __slots__ = ['context']

    def __init__(self, context) -> None:
        super().__init__()
        self.context = context

    @abstractmethod
    def trigger(self, event: str) -> None:
        pass

    def raise_error(self, error_msg: TokenErrMsg) -> None:
        raise TokenError(
            error_msg,
            PositionInCode(
                self.context.code_source.char_row_no,
                self.context.code_source.char_column_no
            )
        )
