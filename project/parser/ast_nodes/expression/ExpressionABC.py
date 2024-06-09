from __future__ import annotations

from abc import abstractmethod

from project.parser.ast_nodes.StatementABC import StatementABC

from project.PositionInCode import PositionInCode


class ExpressionABC(StatementABC):
    @abstractmethod
    def __init__(
        self,
        position: PositionInCode,
    ) -> None:
        super().__init__(position)
