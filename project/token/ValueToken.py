from project.token.Token import Token
from project.token.NoValToken import NoValToken
from project.token.TokenType import TokenType
from project.PositionInCode import PositionInCode


class ValueToken(Token):
    def __init__(
        self,
        type: TokenType,
        value: str | int | float,
        position: PositionInCode
    ) -> None:
        super().__init__(type, position)
        self.value = value

    def __eq__(self, other: Token) -> bool:
        if isinstance(other, NoValToken):
            return super().__eq__(other)
        else:
            return (super().__eq__(other)
                    and self.value == other.value)

    def __str__(self) -> str:
        return super().__str__() + f', value: "{self.value}"'
