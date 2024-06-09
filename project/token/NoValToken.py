from project.token.Token import Token
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode


class NoValToken(Token):
    def __init__(
        self,
        type: TokenType,
        position: PositionInCode
    ) -> None:
        super().__init__(type, position)

    def __eq__(self, other: Token) -> bool:
        return super().__eq__(other)

    def __str__(self) -> str:
        return super().__str__()
