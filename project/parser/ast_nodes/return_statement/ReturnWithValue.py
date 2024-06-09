from typing import Optional

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.parser.ast_nodes.return_statement.ReturnABC import ReturnABC

from project.PositionInCode import PositionInCode


class ReturnWithValue(ReturnABC):
    def __init__(
        self,
        position: PositionInCode,
        value: Optional[ExpressionABC]
    ) -> None:
        super().__init__(position)
        self.value = value

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_return_with_value(self)