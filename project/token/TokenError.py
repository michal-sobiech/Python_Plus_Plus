from project.token.TokenErrorMsg import TokenErrMsg
from project.PositionInCode import PositionInCode


class TokenError(Exception):
    def __init__(
        self,
        error_code: TokenErrMsg,
        position: PositionInCode
    ) -> None:
        self.error_code = error_code
        self.position = position
        super().__init__(str(error_code))
