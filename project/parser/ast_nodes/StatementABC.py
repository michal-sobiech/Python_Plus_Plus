from abc import abstractmethod

from project.parser.ast_nodes.FunDefOrStatementABC import FunDefOrStatementABC

from project.PositionInCode import PositionInCode


class StatementABC(FunDefOrStatementABC):
    @abstractmethod
    def __init__(
        self,
        position: PositionInCode
    ) -> None:
        super().__init__(position)
