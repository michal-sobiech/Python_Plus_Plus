from __future__ import annotations

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class AdditionTerm(ExpressionABC):
    def __init__(
        self,
        position: PositionInCode,
        left_term: ExpressionABC,
        right_term: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.left_term = left_term
        self.right_term = right_term

    def accept(self, interpreter_visitor) -> None:
        interpreter_visitor.visit_addition_term(self)
