from __future__ import annotations
from abc import ABC, abstractmethod

from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode


class Token(ABC):
    def __init__(
        self,
        type: TokenType,
        position: PositionInCode
    ) -> None:
        self.type = type
        self.position = position

    @abstractmethod
    def __eq__(self, other: Token) -> bool:
        return (self.type == other.type
                and self.position == other.position)

    @abstractmethod
    def __str__(self) -> str:
        return '{:<30}, row {}, column {}'.format(
            self.type, self.position.row_no, self.position.column_no)
