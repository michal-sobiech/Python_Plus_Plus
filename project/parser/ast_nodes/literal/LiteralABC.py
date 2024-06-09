from abc import abstractmethod

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class LiteralABC(ExpressionABC):
    @abstractmethod
    def __init__(
        self,
        position: PositionInCode,
        value
    ) -> None:
        super().__init__(position)
        self.value = value
