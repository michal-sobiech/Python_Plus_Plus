from project.parser.ast_nodes.StatementABC import StatementABC
from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class IncrDecrStatementABC(StatementABC):
    def __init__(
        self,
        position: PositionInCode,
        expression: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.expression = expression
