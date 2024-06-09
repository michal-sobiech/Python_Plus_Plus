from project.parser.exceptions.SyntaxErrorMsg import SyntaxErrorMsg

from project.PositionInCode import PositionInCode


class SyntaxError(Exception):
    def __init__(
        self,
        code: SyntaxErrorMsg,
        position: PositionInCode
    ) -> None:
        super().__init__()
        self.code = code
        self.position = position
