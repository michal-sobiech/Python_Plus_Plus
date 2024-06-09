from __future__ import annotations

from abc import abstractmethod

from project.parser.ast_nodes.expression.ExpressionABC import ExpressionABC

from project.PositionInCode import PositionInCode


class CompTermABC(ExpressionABC):
    @abstractmethod
    def __init__(
        self,
        position: PositionInCode,
        left_term: ExpressionABC,
        right_term: ExpressionABC
    ) -> None:
        super().__init__(position)
        self.left_term = left_term
        self.right_term = right_term
